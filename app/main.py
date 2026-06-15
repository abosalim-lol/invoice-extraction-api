from fastapi import FastAPI
from app.routes import extract

app = FastAPI(
    title="Invoice Extraction API",
    description="MVP Invoice Extraction API using OCR and LLMs",
    version="1.0.0"
)

app.include_router(extract.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)