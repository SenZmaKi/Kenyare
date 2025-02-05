export type QuotationInput = {
  is_profitable: boolean;
  financial_summary: string;
  reinsured_name: string;
  broker_name: string;
  insured_name: string;
  partners_count: number;
  qualified_assistants_count: number;
  unqualified_assistants_count: number;
  others_count: number;
  annual_fees: number;
  limit_of_indemnity: number;
  profession: string;
  loss_of_documents: boolean;
  libel_and_slander: boolean;
  dishonest_employees: boolean;
  retroactive_cover: boolean;
};
export type NullableQuotationInput = {
  [K in keyof QuotationInput]: QuotationInput[K] | null;
};
export type RateValueOriginal = {
  rate: number;
  value: number;
  original: any;
};

export type UserQuotationInput = {
  [K in keyof QuotationInput]: K extends
  | "qualified_assistants_count"
  | "unqualified_assistants_count"
  | "others_count"
  | "annual_fees"
  | "limit_of_indemnity"
  | "partners_count"
  ? string
  : QuotationInput[K];
};

export type QuotationOutput = {
  input: QuotationInput;
  partners: RateValueOriginal;
  qualified_assistants: RateValueOriginal;
  unqualified_assistants: RateValueOriginal;
  others: RateValueOriginal;
  annual_fees: RateValueOriginal;
  A: number;
  B: number;
  C: number;
  limit_of_indemnity: RateValueOriginal;
  profession: RateValueOriginal;
  profession_is_confident: boolean;
  A_B_C: number;
  loss_of_documents: number;
  libel_and_slander: number;
  dishonest_employees: number;
  basic_premium: number;
  levies: number;
  sd: number;
  total_premium: number;
  excel_download_url: string;
};


export const testQuotationInput: QuotationInput = {
  is_profitable: true,
  financial_summary:
    "For the year ended 31 December 2022, FEKAN Howell and Associates reported a profit before tax of KSh 12,054,644, a significant increase from KSh 3,168,441 in 2021. The revenue reported was KSh 51,513,198, primarily generated from assurance, consultancy, and training services. Administrative and operating expenses totaled KSh 38,025,243, indicating effective cost management. The organization's financial position reflects a healthy balance with assets exceeding liabilities, ensuring a robust capacity for future growth",
  reinsured_name: "FEKAN HOWELL",
  broker_name: "RSI",
  insured_name: "FIRST ASSURANCE",
  partners_count: 3,
  qualified_assistants_count: 7,
  unqualified_assistants_count: 0,
  others_count: 0,
  annual_fees: 70_000_000,
  limit_of_indemnity: 100_000_000,
  profession:
    "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
  loss_of_documents: true,
  libel_and_slander: true,
  dishonest_employees: true,
  retroactive_cover: false,
};

export const testQuotationOutput: QuotationOutput = {
  input: testQuotationInput,
  partners: {
    rate: 3600,
    value: 10800.0,
    original: 3,
  },
  qualified_assistants: {
    rate: 3000,
    value: 21000.0,
    original: 7,
  },
  unqualified_assistants: {
    rate: 2000,
    value: 0.0,
    original: 0,
  },
  others: {
    rate: 1000,
    value: 0.0,
    original: 0,
  },
  annual_fees: {
    rate: 0.00115,
    value: 80500.0,
    original: 100000000,
  },
  A: 112300.0,
  B: 505350.0,
  C: 505350.0,
  limit_of_indemnity: {
    rate: 4.5,
    value: 505350.0,
    original: 100000000,
  },
  profession: {
    rate: 1,
    value: 505350.0,
    original:
      "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
  },
  profession_is_confident: true,
  A_B_C: 1123000.0,
  loss_of_documents: 112300.0,
  libel_and_slander: 112300.0,
  dishonest_employees: 112300.0,
  basic_premium: 1459900.0,
  levies: 6259.5,
  sd: 40,
  total_premium: 1466199.5,
  excel_download_url: "/outputs/quotation.xlsx",
};