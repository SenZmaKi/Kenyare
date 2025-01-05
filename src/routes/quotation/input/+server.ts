import { json, error, type RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { API_BASE_URL, DELETE_UPLOADS, FINANCIAL_AUDITS_DIR, PROPOSAL_FORMS_DIR } from '$lib/consts';
import { randomUUID } from 'crypto';
import type { QuotationInput } from '$lib/types';

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

    const proposalFormFile = data.get('proposalForm');
    if (!proposalFormFile) throw error(400, 'No proposal form file found');
    const financialAuditFiles = data.getAll('financialAudit');
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

    // Add error handling for the response
    if (!resp.ok) {
        const errorText = await resp.text();
        console.error('API Error:', errorText);
        throw error(resp.status, `API request failed: ${errorText}`);
    }

    const resp_json = await resp.json();
    
    // Log the full response for debugging
    console.log('Full API Response:', JSON.stringify(resp_json, null, 2));

    // Add null checks
    if (!resp_json || !resp_json.data) {
        throw error(500, 'Invalid response format from API');
    }

    const quotation_input: QuotationInput = resp_json.data.quotation_input;
    
    if (!quotation_input) {
        throw error(500, 'No quotation_input found in API response');
    }

    console.log(`quotation_input: ${JSON.stringify(quotation_input)}`);
    return json({
        data: { quotation_input }
    });
}