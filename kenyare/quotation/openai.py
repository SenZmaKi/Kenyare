import json
import os
import logging
from typing import Callable
from dotenv import load_dotenv
import openai
import base64
from io import BytesIO
from PIL import Image
import time
import pdf2image

from kenyare.quotation.common import QuotationInput


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenAI")
IMAGE_FORMAT = "jpeg"

PROMPT = """
    The following documents are the financial audits and accounts and the insurance proposal form of an organization. 
    Take into account some of the information on the documents may be handwritten.
    Extract the following information in json format.
    Restrict yourself to the provided json format and fields, ensure the json is flat, no nesting fields, just one layer deep.
    If you can't extract the data then set the values to default i.e., default string is empty string, default boolean is false, default number is 0.

    json format start
    is_profitable: bool # Determine whether the organization is profitable
    financial_summary: str # An in-depth financial breakdown of the organization, go into detail, one paragraph
    insured_name: str # The name of the person/organization seeking insurance
    reinsured_name: str # The name of the organization seeking reinsurance
    broker_name: str
    partners_count: int # The number of principals/partners in the insured organization
    qualified_assistants_count: int # The number of qualified assistants in the insured organization
    unqualified_assistants_count: int # The number of unqualified assistants in the insured organization
    others_count: int # The number of other employees in the insured organzation
    annual_fees: float # The estimated annual earnings of the insured organization
    limit_of_indemnity: float # The proposed limit of indemnity by the insured organization
    profession: str # The main profession of the insured organization
    loss_of_documents: bool # Whether the insurance should cover loss of documents
    libel_and_slander: bool # Whether the insurance should cover libel and slander
    dishonest_employees: bool # Whether the insurance should cover employee dishonesty
    retroactive_cover: bool # Whether the cover is retroactive
    json format end

    """


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


def run_prompt(doc_paths: list[str]) -> QuotationInput:
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
        model="gpt-4o-mini",
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
                "content": "You are an underwriting assistant for Kenya Reinsurance Corporation (KRC).",
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
