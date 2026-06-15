import os
import tempfile
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty file name")
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check file size by reading first chunk (prevents loading huge files into memory)
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    
    if size == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 10MB limit")

def save_to_temp(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    # Create a named temporary file that deletes on close, but we keep it open
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    temp.write(file.file.read())
    temp.close()
    return temp.name

def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)