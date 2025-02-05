from typing import Any, TypedDict


class QuotationInput(TypedDict):
    is_profitable: bool
    financial_summary: str

    insured_name: str
    reinsured_name: str
    broker_name: str
    partners_count: int
    qualified_assistants_count: int
    unqualified_assistants_count: int
    others_count: int
    annual_fees: float
    limit_of_indemnity: float
    profession: str
    loss_of_documents: bool
    libel_and_slander: bool
    dishonest_employees: bool
    retroactive_cover: bool


class NullableQuotationInput(TypedDict):
    is_profitable: bool | None
    financial_summary: str | None

    insured_name: str | None
    reinsured_name: str | None
    broker_name: str | None
    partners_count: int | None
    qualified_assistants_count: int | None
    unqualified_assistants_count: int | None
    others_count: int | None
    annual_fees: float | None
    limit_of_indemnity: float | None
    profession: str | None
    loss_of_documents: bool | None
    libel_and_slander: bool | None
    dishonest_employees: bool | None
    retroactive_cover: bool | None


class RateValueOriginal(TypedDict):
    rate: float
    value: float
    original: Any


class QuotationOutput(TypedDict):
    input: QuotationInput
    partners: RateValueOriginal
    qualified_assistants: RateValueOriginal
    unqualified_assistants: RateValueOriginal
    others: RateValueOriginal
    annual_fees: RateValueOriginal
    A: float
    B: float
    C: float
    limit_of_indemnity: RateValueOriginal
    profession: RateValueOriginal
    profession_is_confident: bool
    A_B_C: float
    loss_of_documents: float
    libel_and_slander: float
    dishonest_employees: float
    basic_premium: float
    levies: float
    sd: float
    total_premium: float
    excel_download_url: str

test_nullable_quotation_input: NullableQuotationInput = {
    "is_profitable": True,
    "financial_summary": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
    "insured_name": "FEKAN HOWELL",
    "reinsured_name": None,
    "broker_name": "RSI",
    "partners_count": 3,
    "qualified_assistants_count": 7,
    "unqualified_assistants_count": 0,
    "others_count": 0,
    "annual_fees": 70_000_000,
    "limit_of_indemnity": 10,
    "profession": "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
    "loss_of_documents": True,
    "libel_and_slander": True,
    "dishonest_employees": None,
    "retroactive_cover": False,
}


test_quotation_input: QuotationInput = {
    "is_profitable": True,
    "financial_summary": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
    "insured_name": "FEKAN HOWELL",
    "reinsured_name": "FIRST ASSURANCE",
    "broker_name": "RSI",
    "partners_count": 3,
    "qualified_assistants_count": 7,
    "unqualified_assistants_count": 0,
    "others_count": 0,
    "annual_fees": 70_000_000,
    "limit_of_indemnity": 100_000_000,
    "profession": "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
    "loss_of_documents": True,
    "libel_and_slander": True,
    "dishonest_employees": True,
    "retroactive_cover": False,
}
