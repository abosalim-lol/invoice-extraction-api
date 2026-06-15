import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from fastapi import HTTPException

def extract_text_from_file(filepath: str, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            # Convert PDF pages to images
            images = convert_from_path(filepath, dpi=300)
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
        else:
            # Process JPG/PNG directly
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            
        if not text.strip():
            raise HTTPException(status_code=500, detail="OCR failed: No text extracted from document")
            
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")