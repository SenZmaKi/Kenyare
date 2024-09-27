import { json, error, type RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { execSync } from "child_process";
import type { QuotationInput } from '$lib/types';

export async function POST(event: RequestEvent) {
    const data = await event.request.formData()
    const file = data.get('file') as File;

    if (!file) {
        throw error(400, 'No file uploaded');
    }
    const fileName = "input.pdf"
    const uploadPath = path.join('uploads', fileName);
    const arrayBuffer = await file.arrayBuffer();
    fs.writeFileSync(uploadPath, Buffer.from(arrayBuffer), { encoding: 'binary' });
    const output = execSync("python -m kenyare.quotation.input", { encoding: 'utf-8', });
    console.log("Executed python input");
    const quotationInput: QuotationInput = JSON.parse(output);
    const test = {
        reinsured_name: "FIRST ASSURANCE",
        broker_name: "RSI",
        insured_name: "FEKAN HOWELL",
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
        dishonest_employer: true,
        retroactive_cover: true,
    };


    return json({
        success: true,
        data: { "quotation_input": test, "test": quotationInput }
    });
}