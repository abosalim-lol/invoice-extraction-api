from openai import OpenAI
from app.config import settings
from app.schemas.invoice import InvoiceData
from fastapi import HTTPException

# Point the OpenAI client to Groq's API endpoint
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.LLM_BASE_URL,
)

def extract_invoice_data(ocr_text: str) -> dict:
    try:
        # Get the JSON schema of our Pydantic model to show the LLM exactly what we want
        schema_json = InvoiceData.model_json_schema()
        
        completion = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert invoice data extraction assistant. "
                        "Extract the requested fields from the provided OCR text. "
                        "If a field is not found, return an empty string or 0.0. "
                        f"You MUST respond with valid JSON matching this exact schema: {schema_json}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract invoice data from this text:\n\n{ocr_text}"
                }
            ],
            response_format={"type": "json_object"}, # Forces the model to output valid JSON
        )
        
        raw_json = completion.choices[0].message.content
        
        # Parse the JSON string into our Pydantic model to ensure it's valid
        parsed_data = InvoiceData.model_validate_json(raw_json)
        
        # Return as a standard dictionary
        return parsed_data.model_dump()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")