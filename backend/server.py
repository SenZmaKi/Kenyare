from flask import Flask, request, jsonify
from backend.excel import make_excel
from backend.extract import extract_extensions
from backend.quotation import get_quotation
from pathlib import Path
import os

port = int(os.getenv("FLASK_PORT", 5000))
app = Flask(__name__)
upload_folder = Path("uploads")
excels_folder = Path("excels")


def init_server():
    if not upload_folder.is_dir():
        upload_folder.mkdir(parents=True)
    if not excels_folder.is_dir():
        excels_folder.mkdir(parents=True)


@app.route("/api/v1/quotation", methods=["POST"])
def quotation():
    pdf = request.files.get("input.pdf", None)
    if not pdf:
        return "No file selected", 400
    pdf_path = upload_folder / "input.pdf"
    pdf.save(pdf_path)
    input = request.get_json()
    extensions = extract_extensions(pdf_path)
    if not input["loss_of_documents"]:
        input["loss_of_documents"] = extensions["loss_of_documents"]
    if not input["libel_and_slander"]:
        input["libel_and_slander"] = extensions["defamation"]
    if not input["dishonest_employer"]:
        input["dishonest_employer"] = extensions["defamation"]
    output = get_quotation(input)
    excel_file_name = (
        f"{input["reinsured_name"]}-{input['broker_name']}-{input['insured_name']}.xlsx"
    )
    excel_path = excels_folder / excel_file_name
    make_excel(
        input["reinsured_name"],
        input["broker_name"],
        input["insured_name"],
        output,
        excel_path,
    )
    output["excel_file_path"] = str(excel_path.absolute()) # type: ignore
    return jsonify(output)


if __name__ == "__main__":
    init_server()
    app.run(debug=True, port=port)