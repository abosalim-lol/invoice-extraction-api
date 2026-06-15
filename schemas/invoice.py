from pydantic import BaseModel, Field
from typing import Optional

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = Field(default="", description="Invoice number")
    invoice_date: Optional[str] = Field(default="", description="Invoice date")
    vendor_name: Optional[str] = Field(default="", description="Vendor name")
    customer_name: Optional[str] = Field(default="", description="Customer name")
    currency: Optional[str] = Field(default="", description="Currency code (e.g., USD, EUR)")
    subtotal: float = Field(default=0.0, description="Subtotal amount")
    tax: float = Field(default=0.0, description="Tax amount")
    total: float = Field(default=0.0, description="Total amount")

class ExtractionResponse(BaseModel):
    invoice_number: str = ""
    invoice_date: str = ""
    vendor_name: str = ""
    customer_name: str = ""
    currency: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0