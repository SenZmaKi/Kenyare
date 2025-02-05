**Prompt:**

You have access to the financial audit, accounts, and insurance proposal form of an organization.
Your task is to extract the specified information and provide it in the exact JSON format below. Please follow these rules:

1. **Data Extraction**: Ensure that the data you extract is as accurate as possible based on the provided documents. If you are unable to extract or interpret any information clearly, set the value to `null`.
2. **Strictness**: Be as strict as possible with the data. Do not make assumptions or fabricate values. Only include data that you can clearly extract from the documents. If even the least bit unsure, set it to `null`.
3. **JSON Format**: Follow the specified JSON structure. The output should be a flat JSON object, with no nested fields.
4. **Handwriitten text**: Some of the data may be handwritten i.e., a human being may have been given a physical form to fill in.

Here is the required JSON format:

```json
{
  "is_profitable": "boolean | null", // Is the organization profitable based on your own assessment
  "financial_summary": "string | null", // A summary of the organization's financial status based on your own assessment (one paragraph)
  "insured_name": "string | null", // Name of the organization seeking insurance
  "reinsured_name": "string | null", // Name of the organization seeking reinsurance
  "broker_name": "string | null", // Name of the broker involved
  "partners_count": "integer | null", // Number of partners or principals or directors in the insured organization. Sometimes listed by name line by line
  "qualified_assistants_count": "integer | null", // Number of qualified assistants in the insured organization
  "unqualified_assistants_count": "integer | null", // Number of unqualified assistants in the insured organization
  "others_count": "integer | null", // Number of other employees in the insured organization
  "annual_fees": "float | null", // Estimated annual earnings of the insured organization
  "limit_of_indemnity": "float | null", // Proposed limit of indemnity by the insured organization
  "profession": "string | null", // Main profession of the insured organization
  "loss_of_documents": "boolean | null", // Should insurance cover loss of documents?
  "libel_and_slander": "boolean | null", // Should insurance cover libel and slander? Sometimes called defamation
  "dishonest_employees": "boolean | null", // Should insurance cover employee dishonesty?
  "retroactive_cover": "boolean | null" // Is the insurance coverage retroactive?
}
```
