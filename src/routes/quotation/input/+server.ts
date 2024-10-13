import { json } from '@sveltejs/kit';
import { testQuotationInput, type QuotationInput } from '$lib/types';
import { API_BASE_URL } from '$lib/consts';

export async function GET() {
    const resp = await fetch(`${API_BASE_URL}/quotation/input`)
    const resp_json = await resp.json();
    const quotation_input: QuotationInput = resp_json.data.quotation_input;
    // const quotation_input = testQuotationInput;
    console.log(`quotation_input: ${JSON.stringify(quotation_input)}`);
    return json({
        data: { quotation_input }
    });

}