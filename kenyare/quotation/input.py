import json
from pathlib import Path
from typing import TypedDict
import PIL.Image
import pdf2image
import PIL
import pytesseract
import re
from kenyare.quotation.common import QuotationInput

type CropBox = tuple[int, int, int, int]


class Constants:
    defamation_yes = (1086, 830, 1152, 901)
    defamation_no = (1241, 837, 1304, 900)
    loss_of_documents_yes = (1071, 905, 1142, 968)
    loss_of_documents_no = (1237, 919, 1305, 973)
    retroactive_yes = (1079, 994, 1149, 1058)
    retroactive_no = (1235, 991, 1302, 1054)


def get_image_pixel_sum(image: PIL.Image.Image, box: CropBox) -> float:
    cropped_image = image.crop(box)
    grayscale_image = cropped_image.convert("L")
    pixels = grayscale_image.getdata()
    result = sum(pixels)  # type: ignore
    return result


def is_yes(image: PIL.Image.Image, yes_box: CropBox, no_box: CropBox) -> bool:
    yes_sum = get_image_pixel_sum(image, yes_box)
    no_sum = get_image_pixel_sum(image, no_box)
    return yes_sum > no_sum


class Extensions(TypedDict):
    defamation: bool
    loss_of_documents: bool
    retroactive: bool


def extract_extensions(pages: list[PIL.Image.Image]) -> Extensions:
    image = pages[4]
    defamation = is_yes(image, Constants.defamation_yes, Constants.defamation_no)
    loss_of_documents = is_yes(
        image, Constants.loss_of_documents_yes, Constants.loss_of_documents_no
    )
    retroactive = is_yes(image, Constants.retroactive_yes, Constants.retroactive_no)
    return Extensions(
        defamation=defamation,
        loss_of_documents=loss_of_documents,
        retroactive=retroactive,
    )


def extract_quotation_input(pdf_path: Path) -> QuotationInput:
    pages = pdf2image.convert_from_path(pdf_path)
    extensions = extract_extensions(pages)
    pdf_text = "None" or "\n".join(pytesseract.image_to_string(page) for page in pages)
    insured_name_regex = re.search(
        r"(?:insured|insurer|insurance):?\s*(.*)", pdf_text, re.IGNORECASE
    )
    reinsured_name_regex = re.search(
        r"(?:reinsured|reinsurer|reinsurance):?\s*(.*)", pdf_text, re.IGNORECASE
    )
    broker_name_regex = re.search(
        r"(?:broker|insurance company):?\s*(.*)", pdf_text, re.IGNORECASE
    )
    partners_count_regex = re.search(
        r"(?:partners count|partners):?\s*\d+", pdf_text, re.IGNORECASE
    )
    qualified_assistants_count_regex = re.search(
        r"(?:qualified assistants|qualified staff):?\s*\d+", pdf_text, re.IGNORECASE
    )
    unqualified_assistants_count_regex = re.search(
        r"(?:unqualified assistants|unqualified staff):?\s*\d+", pdf_text, re.IGNORECASE
    )
    others_count_regex = re.search(
        r"(?:others|other staff):?\s*\d+", pdf_text, re.IGNORECASE
    )
    annual_fees_regex = re.search(
        r"(?:annual_fees|fees over year|revenue had):?\s*[\d,]+", pdf_text, re.IGNORECASE
    )
    limit_of_indemnity_regex = re.search(
        r"(?:limit of indemnity|indemnity limit):?\s*[\d,]+", pdf_text, re.IGNORECASE
    )
    profession_regex = re.search(
        r"(?:profession|professional services):?\s*(.*)", pdf_text, re.IGNORECASE
    )
    loss_of_documents_regex = re.search(
        r"(?:loss of documents):?\s*(yes|no|true|false)", pdf_text, re.IGNORECASE
    )
    libel_and_slander_regex = re.search(
        r"(?:libel and slander):?\s*(yes|no|true|false)", pdf_text, re.IGNORECASE
    )
    dishonest_employer_regex = re.search(
        r"(?:dishonest employer|employee dishonesty):?\s*(yes|no|true|false)",
        pdf_text,
        re.IGNORECASE,
    )
    insured_name = insured_name_regex.group(1) if insured_name_regex else None
    reinsured_name = reinsured_name_regex.group(1) if reinsured_name_regex else None
    broker_name = broker_name_regex.group(1) if broker_name_regex else None
    partners_count = int(partners_count_regex.group(1) if partners_count_regex else 0)
    qualified_assistants_count = int(
        qualified_assistants_count_regex.group(1)
        if qualified_assistants_count_regex
        else 0
    )
    unqualified_assistants_count = int(
        unqualified_assistants_count_regex.group(1)
        if unqualified_assistants_count_regex
        else 0
    )
    others_count = int(others_count_regex.group(1) if others_count_regex else 0)
    annual_fees = float(annual_fees_regex.group(1) if annual_fees_regex else 0)
    limit_of_indemnity = float(
        limit_of_indemnity_regex.group(1) if limit_of_indemnity_regex else 0
    )
    profession = profession_regex.group(1) if profession_regex else None
    return QuotationInput(
        insured_name=insured_name,  # type: ignore
        reinsured_name=reinsured_name,  # type: ignore
        broker_name=broker_name,  # type: ignore
        partners_count=partners_count,
        qualified_assistants_count=qualified_assistants_count,
        unqualified_assistants_count=unqualified_assistants_count,
        others_count=others_count,
        annual_fees=annual_fees,
        limit_of_indemnity=limit_of_indemnity,
        profession=profession,  # type: ignore
        loss_of_documents=extensions["loss_of_documents"], 
        libel_and_slander=extensions["defamation"], 
        dishonest_employer=extensions["defamation"],
        retroactive=extensions["retroactive"],
    )


def main():
    path = Path("uploads/input.pdf")
    quotation_input = extract_quotation_input(path)
    print(json.dumps(quotation_input, indent=4))


if __name__ == "__main__":
    main()
