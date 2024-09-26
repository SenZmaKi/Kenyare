from typing import Any, TypedDict


class Constants:
    partner_rate = 3600
    qualified_assistant_rate = 3000
    unqualified_assistants_rate = 2000
    other_rate = 1000
    # TODO: Confirm whether this is used to calculate extensions cost or they're just A
    extensions_rate = 0.1
    levies = 6259.50
    sd = 40

    @staticmethod
    def get_annual_fees_rate(annual_fees: float) -> float:
        match annual_fees:
            case annual_fees if annual_fees < 1_000_000:
                return 0.0150
            case annual_fees if annual_fees < 2_000_000:
                return 0.01050
            case annual_fees if annual_fees < 5_000_000:
                return 0.00750
            case annual_fees if annual_fees < 10_000_000:
                return 0.00450
            case annual_fees if annual_fees < 20_000_000:
                return 0.00350
            case annual_fees if annual_fees < 50_000_000:
                return 0.00225
            case _:
                return 0.00115

    @staticmethod
    def get_limit_of_indemnity_rate(limit_of_indemnity: float) -> float:
        match limit_of_indemnity:
            case limit_of_indemnity if limit_of_indemnity < 1_000_000:
                return 1
            case limit_of_indemnity if limit_of_indemnity < 2_500_000:
                return 1.5
            case limit_of_indemnity if limit_of_indemnity < 5_000_000:
                return 1.9
            case limit_of_indemnity if limit_of_indemnity < 10_000_000:
                return 2.3
            case limit_of_indemnity if limit_of_indemnity < 20_000_000:
                return 2.75
            case limit_of_indemnity if limit_of_indemnity < 40_000_000:
                return 3.25
            case limit_of_indemnity if limit_of_indemnity < 60_000_000:
                return 3.65
            case _:
                return 4.5

    @staticmethod
    def get_profession_rate(profession: str) -> tuple[float, bool]:
        profession_lower = profession.lower()

        def is_profession(professions: list[str]) -> bool:
            return any(p in profession_lower for p in professions)

        match profession_lower:
            case profession_lower if is_profession(
                ["optician", "chemist", "tax", "audit", "account", "attorney"]
            ):
                return 1, True
            case profession_lower if is_profession(["civil engineer", "architect"]):
                return 1.35, True
            case profession_lower if is_profession(["dentist", "surgeon", "doctor"]):
                return 1.75, True
            case _:
                return 1.5, False


class QuotationInput(TypedDict):
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


def get_quotation(input: QuotationInput) -> QuotationOutput:
    partners = float(input["partners_count"] * Constants.partner_rate)
    qualified_assistants = float(
        input["qualified_assistants_count"] * Constants.qualified_assistant_rate
    )
    unqualified_assistants = float(
        input["unqualified_assistants_count"] * Constants.unqualified_assistants_rate
    )
    others = float(input["others_count"] * Constants.other_rate)
    annual_fees_rate = Constants.get_annual_fees_rate(input["annual_fees"])
    annual_fees = annual_fees_rate * input["annual_fees"]
    A = partners + qualified_assistants + unqualified_assistants + others + annual_fees
    limit_of_indemnity_rate = Constants.get_limit_of_indemnity_rate(
        input["limit_of_indemnity"]
    )
    limit_of_indemnity = A * limit_of_indemnity_rate
    B = limit_of_indemnity
    profession_rate, profession_is_confident = Constants.get_profession_rate(
        input["profession"]
    )
    profession = profession_rate * B
    C = profession
    A_B_C = A + B + C
    loss_of_documents = A if input["loss_of_documents"] else None
    libel_and_slander = A if input["libel_and_slander"] else None
    dishonest_employer = A if input["dishonest_employer"] else None
    basic_premium = A_B_C
    if loss_of_documents:
        basic_premium += loss_of_documents
    if libel_and_slander:
        basic_premium += libel_and_slander
    if dishonest_employer:
        basic_premium += dishonest_employer
    total_premium = basic_premium + Constants.levies + Constants.sd
    return QuotationOutput(
        partners={
            "rate": Constants.partner_rate,
            "value": partners,
            "original": input["partners_count"],
        },
        qualified_assistants={
            "rate": Constants.qualified_assistant_rate,
            "value": qualified_assistants,
            "original": input["qualified_assistants_count"],
        },
        unqualified_assistants={
            "rate": Constants.unqualified_assistants_rate,
            "value": unqualified_assistants,
            "original": input["unqualified_assistants_count"],
        },
        others={
            "rate": Constants.other_rate,
            "value": others,
            "original": input["others_count"],
        },
        annual_fees={
            "rate": annual_fees_rate,
            "value": annual_fees,
            "original": input["annual_fees"],
        },
        A=A,
        B=B,
        C=C,
        limit_of_indemnity={
            "rate": limit_of_indemnity_rate,
            "value": limit_of_indemnity,
            "original": input["limit_of_indemnity"],
        },
        profession={
            "rate": profession_rate,
            "value": profession,
            "original": input["profession"],
        },
        profession_is_confident=profession_is_confident,
        A_B_C=A_B_C,
        loss_of_documents=loss_of_documents,
        libel_and_slander=libel_and_slander,
        dishonest_employer=dishonest_employer,
        basic_premium=basic_premium,
        levies=Constants.levies,
        sd=Constants.sd,
        total_premium=total_premium,
    )


def test_get_quotation():
    input: QuotationInput = {
        "partners_count": 3,
        "qualified_assistants_count": 7,
        "unqualified_assistants_count": 0,
        "others_count": 0,
        "annual_fees": 70_000_000,
        "limit_of_indemnity": 100_000_000,
        "profession": "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
        "loss_of_documents": True,
        "libel_and_slander": True,
        "dishonest_employer": True,
    }
    output = get_quotation(input)

    print(output)
    assert output["total_premium"] == 1466199.5


if __name__ == "__main__":
    test_get_quotation()
