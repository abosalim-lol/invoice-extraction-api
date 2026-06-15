from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from middleware.api_key import verify_api_key
from utils.files import validate_file, save_to_temp, cleanup_temp_file
from services.ocr import extract_text_from_file
from services.extractor import extract_invoice_data

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/extract", dependencies=[Depends(verify_api_key)])
async def extract_invoice(file: UploadFile = File(...)):
    validate_file(file)
    temp_filepath = None
    
    try:
        temp_filepath = save_to_temp(file)
        ocr_text = extract_text_from_file(temp_filepath, file.filename)
        extracted_data = extract_invoice_data(ocr_text)
        return extracted_data
        
    finally:
        if temp_filepath:
            cleanup_temp_file(temp_filepath)