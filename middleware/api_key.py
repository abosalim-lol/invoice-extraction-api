from fastapi import Request, HTTPException, status
from config import ALLOWED_API_KEYS
import os

async def verify_api_key(request: Request):
    # Debug: Print all headers (check Railway logs)
    print("=== HEADERS RECEIVED ===")
    for key, value in request.headers.items():
        print(f"{key}: {value}")
    print("=======================")
    
    custom_api_key = request.headers.get("x-api-key")
    rapidapi_key = request.headers.get("x-rapidapi-key")
    
    print(f"Custom API Key: {custom_api_key}")
    print(f"RapidAPI Key: {rapidapi_key}")
    
    # Scenario 1: Request is coming through RapidAPI
    if rapidapi_key:
        print("✓ RapidAPI key found - allowing request")
        return
        
    # Scenario 2: Direct request
    if custom_api_key and custom_api_key in ALLOWED_API_KEYS:
        print("✓ Custom API key found and valid - allowing request")
        return
        
    # Block the request
    print("✗ No valid API key found - blocking request")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )