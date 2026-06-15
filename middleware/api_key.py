from fastapi import Request, HTTPException, status
from config import ALLOWED_API_KEYS

async def verify_api_key(request: Request):
    custom_api_key = request.headers.get("x-api-key")
    rapidapi_user = request.headers.get("x-rapidapi-user")
    mashape_user = request.headers.get("x-mashape-user")
    
    # Scenario 1: Request is coming through RapidAPI
    # RapidAPI has already validated the user, so we just check if the user header exists.
    if rapidapi_user or mashape_user:
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