from pathlib import Path
from typing import TypedDict
import PIL.Image
import pdf2image
import PIL

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
    result = sum(pixels) # type: ignore
    return result


def is_yes(image: PIL.Image.Image, yes_box: CropBox, no_box: CropBox) -> bool:
    yes_sum = get_image_pixel_sum(image, yes_box)
    no_sum = get_image_pixel_sum(image, no_box)
    print(yes_sum, no_sum)
    return yes_sum > no_sum


class Extensions(TypedDict):
    defamation: bool
    loss_of_documents: bool
    retroactive: bool


def extract_extensions(pdf_path: Path) -> Extensions:
    pages = pdf2image.convert_from_path(pdf_path)
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


def test_extract_extensions():
    path = Path("input.pdf")
    extensions = extract_extensions(path)
    print(extensions)


if __name__ == "__main__":
    test_extract_extensions()
