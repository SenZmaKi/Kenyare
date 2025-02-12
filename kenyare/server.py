import os
# import sys
# To allow running as a script instead of module i.e., python kenyare/server.py instead of python -m kenyare.server
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import shutil
import uuid
from flask import Flask, request, jsonify
from kenyare.quotation.excel import make_excel
from kenyare.quotation.openai import run_prompt
from kenyare.quotation.output import get_quotation_output
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
QUOTATIONS_DIR = "static/quotations"
if not os.path.exists(QUOTATIONS_DIR):
    os.makedirs(QUOTATIONS_DIR)
if os.getenv("CLEAR_QUOTATIONS_DIR") == "1":
    shutil.rmtree(QUOTATIONS_DIR)
    os.makedirs(QUOTATIONS_DIR)


@app.route("/quotation/input", methods=["POST"])
def quotation_input():
    # from kenyare.quotation.common import test_nullable_quotation_input
    # return jsonify(
    #     {"data": {"nullable_quotation_input": test_nullable_quotation_input}}
    # ), 200
    if not request.json:
        return jsonify({"error": "No JSON in request"}), 400
    proposal_path = request.json["proposal_path"]
    audit_paths = request.json["audit_paths"]
    nullable_quotation_input = run_prompt([*audit_paths, proposal_path])
    return jsonify(
        {"data": {"nullable_quotation_input": nullable_quotation_input}}
    ), 200


@app.route("/quotation/output", methods=["POST"])
def quotation_output():
    if not request.json:
        return jsonify({"error": "No JSON in request"}), 400
    quotation_input = request.json["quotation_input"]
    quotation_output = get_quotation_output(quotation_input)
    excel_filename = f"{uuid.uuid4()}.xlsx"
    excel_path = f"{QUOTATIONS_DIR}/{excel_filename}"
    excel_download_url = f"/quotations/{excel_filename}"
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
    app.run(
        debug=os.getenv("FLASK_DEBUG", "1") == "1",
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", 5000)),
    )
