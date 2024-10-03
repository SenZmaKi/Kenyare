from functools import cache
from typing import TypedDict, cast
import requests
import json
import re

from kenyare.quotation.common import QuotationInput

API_BASE_URL = "https://api.stack-ai.com"
UPLOAD_URL = f"{API_BASE_URL}/upload_to_supabase_user?"
RUN_URL = f"{API_BASE_URL}/run_exported_flow_public?"


class Credentials(TypedDict):
    flow_id: str
    org_id: str
    user_id: str
    node_id: str
    public_api_key: str


@cache
def load_credentials() -> Credentials:
    try:
        with open("kenyare/credentials.json") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                raise Exception("Invalid JSON in credentials.json")
    except FileNotFoundError:
        raise Exception("credentials.json not found")


def upload_file(file_path: str) -> requests.Response:
    creds = load_credentials()

    with open(file_path, "rb") as f:
        flow_id = creds["flow_id"]
        org_id = creds["org_id"]
        user_id = creds["user_id"]
        node_id = creds["node_id"]
        public_api_key = creds["public_api_key"]
        files = {"file": f}
        headers = make_headers(public_api_key)
        upload_url = f"{UPLOAD_URL}flow_id={flow_id}&org={org_id}&user_id={user_id}&node_id={node_id}"
        response = requests.post(upload_url, files=files, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to upload file: {response.text}")

        return response


def run_flow(
    flow_id: str, org_id: str, user_id: str, public_api_key: str
) -> requests.Response:
    headers = make_headers(public_api_key)
    run_url = f"{RUN_URL}flow_id={flow_id}&org={org_id}&mode=outputs"
    response = requests.post(run_url, headers=headers, json={"user_id": user_id})

    if response.status_code != 200:
        raise Exception(f"Failed to run flow: {response.text}")

    return response


def get_quotation_input() -> QuotationInput:
    creds = load_credentials()
    flow_id = creds["flow_id"]
    org_id = creds["org_id"]
    user_id = creds["user_id"]
    public_api_key = creds["public_api_key"]
    flow_response = run_flow(flow_id, org_id, user_id, public_api_key)
    input_match = re.findall(r"\"out-0\":\s*\"({.*?})\"", flow_response.text)[-1]
    input_match = cast(str, input_match)
    input_match = input_match.replace("\\n", "\n").replace("\\", "")
    input_json = json.loads(input_match)
    return input_json


def make_headers(public_api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {public_api_key}",
    }


def test():
    input_path = "uploads/proposal.pdf"
    upload_file(input_path)
    output = get_quotation_input()
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
