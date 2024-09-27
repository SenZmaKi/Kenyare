
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
  dishonest_employer: boolean;
  retroactive_cover: boolean;
};

type RateValueOriginal = {
  rate: number;
  value: number;
  original: any;
};

type QuotationOutput = {
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
  dishonest_employer: number;
  basic_premium: number;
  levies: number;
  sd: number;
  total_premium: number;
  excel_download_url: string;
};
