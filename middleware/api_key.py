from fastapi import Request, HTTPException, status
from config import ALLOWED_API_KEYS

async def verify_api_key(request: Request):
    custom_api_key = request.headers.get("x-api-key")
    rapidapi_key = request.headers.get("x-rapidapi-key")
    
    # Scenario 1: Request is coming through RapidAPI
    # RapidAPI has already validated the user, so we just check if the header exists.
    if rapidapi_key:
        return
        
    # Scenario 2: Direct request (e.g., local testing or direct to Railway)
    # We check if the custom key matches our allowed list.
    if custom_api_key and custom_api_key in ALLOWED_API_KEYS:
        return
        
    # If neither condition is met, block the request
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )