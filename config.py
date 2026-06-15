from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str  # We keep the name, but it's actually the Groq key
    API_KEYS: str 
    
    # Groq Configuration
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MODEL: str = "llama-3.3-70b-versatile" # Extremely fast and smart
    
    class Config:
        env_file = ".env"

settings = Settings()
ALLOWED_API_KEYS = [key.strip() for key in settings.API_KEYS.split(",") if key.strip()]