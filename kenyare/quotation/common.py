from typing import Any, TypedDict


class QuotationInput(TypedDict):
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
    dishonest_employer: bool
    retroactive: bool



class RateValueOriginal(TypedDict):
    rate: float
    value: float
    original: Any


class QuotationOutput(TypedDict):
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
    loss_of_documents: float | None
    libel_and_slander: float | None
    dishonest_employer: float | None
    basic_premium: float
    levies: float
    sd: float
    total_premium: float
