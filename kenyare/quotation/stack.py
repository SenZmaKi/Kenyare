from functools import cache
from base64 import b64encode, b64decode
from typing import TypedDict, cast
import requests
import json
import re
import threading

from kenyare.quotation.common import QuotationInput

API_BASE_URL = "https://api.stack-ai.com"
UPLOAD_URL = f"{API_BASE_URL}/upload_to_supabase_user?"
RUN_URL = f"{API_BASE_URL}/run_exported_flow_public?"


class Credentials(TypedDict):
    flow_id: str
    org_id: str
    user_id: str
    public_api_key: str


def base64_encode_credentials():
    with open("kenyare/credentials.json") as json_creds:
        with open("kenyare/credentials.txt", "w") as base64_creds:
            encoded = b64encode(json_creds.read().encode()).decode()
            base64_creds.write(encoded)


@cache
def load_credentials(from_json=False) -> Credentials:
    if from_json:
        with open("kenyare/credentials.json") as f:
            return json.load(f)
    else:
        with open("kenyare/credentials.txt") as f:
            decoded = b64decode(f.read().encode()).decode()
            return json.loads(decoded)


def upload_file(file_path: str, node_id: str, file_name: str) -> requests.Response:
    creds = load_credentials()

    with open(file_path, "rb") as f:
        flow_id = creds["flow_id"]
        org_id = creds["org_id"]
        user_id = creds["user_id"]
        public_api_key = creds["public_api_key"]
        files = {"file": (file_name, f)}
        headers = make_headers(public_api_key)
        upload_url = f"{UPLOAD_URL}flow_id={flow_id}&org={org_id}&user_id={user_id}&node_id={node_id}"
        response = requests.post(upload_url, files=files, headers=headers)

        if not response.ok:
            raise Exception(f"Failed to upload {file_name}: {response.text}")

        return response


def upload_files(
    proposal_path: str, audit_path: str
) -> tuple[requests.Response, requests.Response]:
    responses: list = [None, None]

    def upload_financial_audit():
        responses[0] = upload_file(audit_path, "doc-0", "financial-audit.pdf")

    def upload_proposal_form():
        responses[1] = upload_file(proposal_path, "doc-1", "proposal-form.pdf")

    proposal_thread = threading.Thread(target=upload_proposal_form)
    audit_thread = threading.Thread(target=upload_financial_audit)

    proposal_thread.start()
    audit_thread.start()

    proposal_thread.join()
    audit_thread.join()
    if not responses[0].ok:
        raise Exception(f"Failed to upload financial audit: {responses[0].text}")
    if not responses[1].ok:
        raise Exception(f"Failed to upload proposal form: {responses[1].text}")

    return responses[0], responses[1]


def run_flow(
    flow_id: str, org_id: str, user_id: str, public_api_key: str
) -> requests.Response:
    headers = make_headers(public_api_key)
    run_url = f"{RUN_URL}flow_id={flow_id}&org={org_id}&mode=outputs"
    response = requests.post(run_url, headers=headers, json={"user_id": user_id})

    if not response.ok:
        raise Exception(f"Failed to run flow: {response.text}")

    return response


def get_quotation_input() -> QuotationInput:
    creds = load_credentials()
    flow_id = creds["flow_id"]
    org_id = creds["org_id"]
    user_id = creds["user_id"]
    public_api_key = creds["public_api_key"]
    flow_response = run_flow(flow_id, org_id, user_id, public_api_key)
    input_match = re.findall(r"\"out-2\":\s*\"({.*?})\"", flow_response.text)[-1]
    input_match = cast(str, input_match)
    input_match = input_match.replace("\\n", "\n").replace("\\", "")
    input_json = json.loads(input_match)
    return input_json


def make_headers(public_api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {public_api_key}",
    }


def test():
    audit_path = "uploads/fekan-audit.pdf"
    proposal_path = "uploads/fekan-proposal.pdf"
    print(f"Uploading {audit_path} and {proposal_path}")
    upload_files(proposal_path, audit_path)
    print("Uploaded!")
    print("Extracting...")
    output = get_quotation_input()
    print("Extracted!")
    # output = {
    #     "insured_name": "FEKAN HOWELL",
    #     "reinsured_name": "FIRST ASSURANCE",
    #     "broker_name": "RSI",
    #     "partners_count": 3,
    #     "qualified_assistants_count": 7,
    #     "unqualified_assistants_count": 0,
    #     "others_count": 0,
    #     "annual_fees": 70_000_000,
    #     "limit_of_indemnity": 100_000_000,
    #     "profession": "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
    #     "loss_of_documents": True,
    #     "libel_and_slander": True,
    #     "dishonest_employees": True,
    #     "retroactive_cover": False,
    # }
    print(json.dumps(output))


if __name__ == "__main__":
    test()
