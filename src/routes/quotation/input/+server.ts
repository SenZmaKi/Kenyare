import { json, error, type RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { API_BASE_URL, DELETE_UPLOADS, FINANCIAL_AUDITS_DIR, PROPOSAL_FORMS_DIR } from '$lib/consts';
import { randomUUID } from 'crypto';
import type { NullableQuotationInput } from '$lib/types';

async function saveFile(file: File, saveDir: string): Promise<string> {
    const fileExtension = file.name.split('.').pop();
    const fileName = `${randomUUID()}.${fileExtension}`;
    const filePath = path.join(saveDir, fileName);
    const arrayBuffer = await file.arrayBuffer();
    const dataView = new DataView(arrayBuffer);
    await fs.promises.writeFile(filePath, dataView);
    return filePath;
}

export async function POST(event: RequestEvent) {
    const data = await event.request.formData();


    const proposalFormFile = data.get('proposal_form');
    if (!proposalFormFile) throw error(400, 'No proposal form file found');
    const financialAuditFiles = data.getAll('financial_audits');
    if (!financialAuditFiles.length) throw error(400, 'No financial audit files found');

    const [proposalFormPath, financialAuditPaths] = await Promise.all([
        saveFile(proposalFormFile as File, PROPOSAL_FORMS_DIR),
        Promise.all(financialAuditFiles.map((f) => saveFile(f as File, FINANCIAL_AUDITS_DIR)))
    ]);

    const resp = await fetch(`${API_BASE_URL}/quotation/input`, {
        method: "POST",
        body: JSON.stringify({
            proposal_path: proposalFormPath,
            audit_paths: financialAuditPaths
        }),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });

    if (DELETE_UPLOADS)
        Promise.all([...financialAuditPaths, proposalFormPath].map(fs.promises.unlink));

    const respJson = await resp.json();
    const nullable_quotation_input: NullableQuotationInput = respJson.data.nullable_quotation_input;
    console.log(`nullable_quotation_input: ${JSON.stringify(nullable_quotation_input)}`);
    return json({
        data: { nullable_quotation_input }
    });

}