from kenyare.quotation.common import QuotationOutput
from openpyxl import load_workbook


def make_excel(
    reinsured_name: str,
    broker_name: str,
    insured_name: str,
    quotation_output: QuotationOutput,
    save_path: str,
):
    workbook = load_workbook("kenyare/quotation/template.xlsx")
    sheet = workbook.active
    if sheet is None:
        raise Exception("Invalid sheet")

    sheet["B4"] = f"REINSURED: {reinsured_name}"
    sheet["B6"] = f"BROKER: {broker_name}"
    sheet["B8"] = f"INSURED: {insured_name}"

    def add_rate_value_original(rate_value_original, row, in_percent=True):
        rate = rate_value_original["rate"]
        if in_percent:
            rate = rate * 100
            rate = f"{rate:.2f}%"
        else:
            rate = f"{rate:.2f}"
        sheet[f"C{row}"] = rate_value_original["original"]
        sheet[f"D{row}"] = rate
        sheet[f"E{row}"] = rate_value_original["value"]

    add_rate_value_original(quotation_output["partners"], 12, False)
    add_rate_value_original(quotation_output["qualified_assistants"], 13, False)
    add_rate_value_original(quotation_output["unqualified_assistants"], 14, False)
    add_rate_value_original(quotation_output["others"], 15, False)
    add_rate_value_original(quotation_output["annual_fees"], 17)

    sheet["E17"] = quotation_output["A"]
    add_rate_value_original(quotation_output["limit_of_indemnity"], 20)
    add_rate_value_original(
        quotation_output["profession"],
        22,
    )
    sheet["E24"] = quotation_output["A_B_C"]
    sheet["E26"] = (
        quotation_output["loss_of_documents"]
        if quotation_output["loss_of_documents"]
        else ""
    )
    sheet["E27"] = (
        quotation_output["libel_and_slander"]
        if quotation_output["libel_and_slander"]
        else ""
    )
    sheet["E28"] = (
        quotation_output["dishonest_employees"]
        if quotation_output["dishonest_employees"]
        else ""
    )
    sheet["E29"] = quotation_output["basic_premium"]
    sheet["E31"] = quotation_output["basic_premium"]
    sheet["E32"] = quotation_output["levies"]
    sheet["E33"] = quotation_output["sd"]
    sheet["E34"] = quotation_output["total_premium"]

    with open(save_path, "w"):
        pass
    workbook.save(save_path)
