import json
import base64
import tempfile
import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Union
from middleware.api_key import verify_api_key
from utils.files import validate_file, save_to_temp, cleanup_temp_file
from services.ocr import extract_text_from_file
from services.extractor import extract_invoice_data

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/extract", dependencies=[Depends(verify_api_key)])
async def extract_invoice(file: Union[UploadFile, str] = File(...)):
    temp_filepath = None
    filename = "unknown.png"
    
    try:
        # Scenario 1: Standard file upload (cURL, Python requests, etc.)
        if isinstance(file, UploadFile):
            validate_file(file)
            filename = file.filename
            temp_filepath = save_to_temp(file)
        
        # Scenario 2: Base64 string / JSON string (RapidAPI playground, some JS clients)
        elif isinstance(file, str):
            # Try to parse as JSON first (RapidAPI sends: {"value": "name.png", "data": "data:image/png;base64,..."})
            try:
                payload = json.loads(file)
                filename = payload.get("value", "unknown.png")
                base64_data = payload.get("data", "")
            except json.JSONDecodeError:
                # If it's just a raw base64 string
                base64_data = file
                
            # Remove the data URI scheme if present (e.g., "data:image/png;base64,")
            if "," in base64_data:
                base64_data = base64_data.split(",", 1)[1]
                
            # Decode base64
            try:
                file_bytes = base64.b64decode(base64_data)
            except Exception as e:
                raise HTTPException(status_code=400, detail="Invalid base64 encoding")
                
            # Determine extension from filename
            ext = os.path.splitext(filename)[1].lower()
            if ext not in {".pdf", ".jpg", ".jpeg", ".png"}:
                ext = ".png" # default fallback
                
            # Save to temp file
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            temp.write(file_bytes)
            temp.close()
            temp_filepath = temp.name
            
        else:
            raise HTTPException(status_code=400, detail="Invalid file format")

        # Process the file
        ocr_text = extract_text_from_file(temp_filepath, filename)
        extracted_data = extract_invoice_data(ocr_text)
        return extracted_data
        
    finally:
        if temp_filepath and os.path.exists(temp_filepath):
            os.remove(temp_filepath)