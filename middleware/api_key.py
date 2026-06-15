from fastapi import Request, HTTPException, status
from config import ALLOWED_API_KEYS

async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in ALLOWED_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key"
        )