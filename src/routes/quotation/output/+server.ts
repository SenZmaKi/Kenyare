import type { QuotationOutput } from '$lib/types';
import { json, type RequestEvent } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/consts';

export async function POST(event: RequestEvent) {
    const req_json = await event.request.json();
    const quotation_input: QuotationOutput = req_json.quotation_input;
    const resp = await fetch(`${API_BASE_URL}/quotation/output`, {
        method: "POST",
        body: JSON.stringify({ quotation_input }),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });
    const resp_json = await resp.json();
    const quotation_output: QuotationOutput = resp_json.data.quotation_output;
    console.log(`quotation_output: ${JSON.stringify(quotation_output)}`);
    return json({
        success: true,
        data: { quotation_output }
    });


}
