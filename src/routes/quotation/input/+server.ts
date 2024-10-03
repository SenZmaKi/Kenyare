import { json, type RequestEvent, error } from '@sveltejs/kit';
import type { QuotationInput } from '$lib/types';
import { API_BASE_URL } from '$lib/consts';

export async function GET(event: RequestEvent) {
    const resp = await fetch(`${API_BASE_URL}/quotation/input`)
    const resp_json = await resp.json();
    const quotation_input: QuotationInput = resp_json.data.quotation_input;
    console.log(`quotation_input: ${JSON.stringify(quotation_input)}`);
    return json({
        data: { quotation_input }
    });

}