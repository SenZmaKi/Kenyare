import os
from flask import Flask, request, jsonify
from kenyare.quotation.excel import make_excel
from kenyare.quotation.stack import get_quotation_input, upload_files
from kenyare.quotation.output import get_quotation_output

app = Flask(__name__)


@app.route("/quotation/upload", methods=["POST"])
def quotation_upload():
    if not request.json:
        return jsonify({"error": "No JSON in request"}), 400
    proposal_path = request.json["proposal_path"]
    audit_path = request.json["audit_path"]
    upload_files(proposal_path, audit_path)
    return jsonify({"data": {}}), 200


@app.route("/quotation/input", methods=["GET"])
def quotation_input():
    quotation_input = get_quotation_input()
    print(f"quotation_input: {quotation_input}")
    return jsonify({"data": {"quotation_input": quotation_input}}), 200


@app.route("/quotation/output", methods=["POST"])
def quotation_output():
    if not request.json:
        return jsonify({"error": "No JSON in request"}), 400
    quotation_input = request.json["quotation_input"]
    quotation_output = get_quotation_output(quotation_input)
    excel_download_url = "/outputs/quotation.xlsx"
    excel_path = f"static{excel_download_url}"
    make_excel(
        quotation_input["reinsured_name"],
        quotation_input["broker_name"],
        quotation_input["insured_name"],
        quotation_output,
        excel_path,
    )
    quotation_output["excel_download_url"] = excel_download_url

    print(f"quotation_output: {quotation_output}")
    return jsonify({"data": {"quotation_output": quotation_output}}), 200


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("FLASK_PORT", 5000)))
