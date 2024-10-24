import { json, error, type RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { API_BASE_URL } from '$lib/consts';

async function saveFile(data: FormData, fileKey: string): Promise<string> {
    const file = data.get(fileKey) as File | null;

    if (!file) throw error(400, `No file found for key: ${fileKey}`);
    const filePath = path.join('uploads', file.name);
    const arrayBuffer = await file.arrayBuffer();
    const dataView = new DataView(arrayBuffer);
    await fs.promises.writeFile(filePath, dataView);
    return filePath;
}

export async function POST(event: RequestEvent) {
    const data = await event.request.formData();

    const [financialAuditPath, proposalFormPath] = await Promise.all([
        saveFile(data, 'financialAudit'),
        saveFile(data, 'proposalForm'),
    ]);

    await fetch(`${API_BASE_URL}/quotation/upload`, {
        method: "POST",
        body: JSON.stringify({
            proposal_path: proposalFormPath,
            audit_path: financialAuditPath
        }),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });

    return json({
        success: true,
        data: {}
    });
}