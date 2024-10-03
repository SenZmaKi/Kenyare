export type QuotationInput = {
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

export type RateValueOriginal = {
  rate: number;
  value: number;
  original: any;
};

export type QuotationOutput = {
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


export const testQuotationOutput = {
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