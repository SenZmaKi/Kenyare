import { json, error, type RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';
import { API_BASE_URL } from '$lib/consts';

export async function POST(event: RequestEvent) {
    const data = await event.request.formData()
    const file = data.get('file') as File;

    if (!file) {
        throw error(400, 'No file uploaded');
    }
    const fileName = "proposal.pdf"
    const file_path = path.join('uploads', fileName);
    const arrayBuffer = await file.arrayBuffer();
    fs.writeFileSync(file_path, Buffer.from(arrayBuffer), { encoding: 'binary' });
    const resp = await fetch(`${API_BASE_URL}/quotation/upload`, {
        method: "POST",
        body: JSON.stringify({ file_path }),
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