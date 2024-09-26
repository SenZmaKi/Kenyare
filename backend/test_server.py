import requests


def test_quotation():
    input = {
        "partners_count": 3,
        "qualified_assistants_count": 7,
        "unqualified_assistants_count": 0,
        "others_count": 0,
        "annual_fees": 70_000_000,
        "limit_of_indemnity": 100_000_000,
        "profession": "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
    }
    with open("input.pdf", "rb") as f:
        response = requests.post(
            "http://localhost:5000/api/v1/quotation",
            data={"input": input, "file": f},
            headers={"Content-Type": "multipart/form-data"},
        )
        print(response.text)
        print(response.status_code)
        assert response.status_code == 200


if __name__ == "__main__":
    test_quotation()
