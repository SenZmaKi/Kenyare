import os
import shutil
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from kenyare.quotation.excel import make_excel
from kenyare.quotation.openai import run_prompt
from kenyare.quotation.output import get_quotation_output

# Create quotations directory
QUOTATIONS_DIR = "static/quotations"
os.makedirs(QUOTATIONS_DIR, exist_ok=True)

# Clear quotations directory if environment variable is set
if os.getenv("CLEAR_QUOTATIONS_DIR") == "1":
    shutil.rmtree(QUOTATIONS_DIR)
    os.makedirs(QUOTATIONS_DIR)

# Create FastAPI app
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class QuotationInputRequest(BaseModel):
    proposal_path: str
    audit_paths: list[str]

class QuotationOutputRequest(BaseModel):
    quotation_input: dict

@app.post("/quotation/input")
async def quotation_upload(request: QuotationInputRequest):
    try:
        quotation_input = run_prompt([*request.audit_paths, request.proposal_path])
        return {"data": {"quotation_input": quotation_input}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quotation/output")
async def quotation_output(request: QuotationOutputRequest):
    try:
        quotation_input = request.quotation_input
        quotation_output = get_quotation_output(quotation_input)
        
        excel_filename = f"{uuid.uuid4()}.xlsx"
        excel_path = f"{QUOTATIONS_DIR}/{excel_filename}"
        excel_download_url = f"/quotations/{excel_filename}"
        
        make_excel(
            quotation_input["reinsured_name"],
            quotation_input["broker_name"],
            quotation_input["insured_name"],
            quotation_output,
            excel_path,
        )
        
        quotation_output["excel_download_url"] = excel_download_url
        
        return {"data": {"quotation_output": quotation_output}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"status": "KenyaRE FASTAPI Server is running!"}

if __name__ == "__main__":
    uvicorn.run(
        "kenyare.server:app", 
        host=os.getenv("SERVER_HOST", "localhost"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )