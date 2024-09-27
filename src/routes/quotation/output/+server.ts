import { json, error, type RequestEvent } from '@sveltejs/kit';
import { execSync } from "child_process";
import { writeFileSync } from "fs";

export async function POST(event: RequestEvent) {
    const req_json = await event.request.json()
    const req_json_str = JSON.stringify(req_json);
    writeFileSync("uploads/quotation_input.json", req_json_str);
    const output = execSync(`python -m kenyare.quotation.output`, { encoding: 'utf-8', });
    console.log("Executed python output");
    const quotationOutput = JSON.parse(output);
    console.log(quotationOutput["excel_download_url"]);
    return json({
        success: true,
        data: { "quotation_output": quotationOutput }
    });

}
