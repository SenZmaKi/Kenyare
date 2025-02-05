import json
import logging
from pathlib import Path
from typing import Callable
from dotenv import load_dotenv
import openai
import base64
from io import BytesIO
from PIL import Image
import time
import pdf2image
from kenyare.quotation.common import NullableQuotationInput

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenAI")

IMAGE_FORMAT = "jpeg"
parent_folder = Path(__file__).parent
PROMPT = (parent_folder / "prompt.md").read_text(encoding="utf-8")
ROLE = (parent_folder / "role.md").read_text(encoding="utf-8")


class OpenAIException(Exception):
    pass


client = openai.OpenAI()
if not client.api_key:
    raise OpenAIException("OPENAI_API_KEY environment variable is not set.")


def print_runtime_later(task: str) -> Callable[[], None]:
    start_time = time.time()

    def print_runtime() -> None:
        elapsed_time = time.time() - start_time
        logger.info(f"Task {task} took {elapsed_time:.2f} seconds.")

    return print_runtime


def image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format=IMAGE_FORMAT.upper())
    img_byte_data = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte_data).decode("utf-8")
    return img_base64


def run_prompt(doc_paths: list[str]) -> NullableQuotationInput:
    logger.info(f"Converting pdfs to images: {doc_paths}")
    prt = print_runtime_later("Convert pdfs to images")
    pdf_images = [
        image
        for doc_path in doc_paths
        for image in pdf2image.convert_from_path(doc_path)
    ]
    prt()
    logger.info(f"Encoding {len(pdf_images)} images to base64")
    prt = print_runtime_later("Encoding images to base64")
    base64_images = [image_to_base64(image) for image in pdf_images]
    prt()
    logger.info(f"Prompting OpenAI with {len(base64_images)} images")
    prt = print_runtime_later("Prompting OpenAI")
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT,
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{IMAGE_FORMAT};base64,{base64_image}",
                            },
                        }
                        for base64_image in base64_images
                    ],
                ],
            },
            {
                "role": "system",
                "content": ROLE,
            },
        ],
    )
    prt()
    output = response.choices[0].message.content
    if not output:
        raise OpenAIException("OpenAI response is empty.")
    logger.info(f"OpenAI response: {output}")
    output_json = json.loads(output)
    return output_json


def main() -> None:
    financial_audit_path = "uploads/fekan-audit.pdf"
    proposal_form_path = "uploads/fekan-proposal.pdf"
    run_prompt([financial_audit_path, proposal_form_path])


if __name__ == "__main__":
    main()
