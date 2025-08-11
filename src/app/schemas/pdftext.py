# src/app/schemas/pdftext.py
from typing import Optional
from pydantic import BaseModel, Field


class PdfTextRequest(BaseModel):
    base64: str = Field(..., description="Base64 do Pdf")
    encod: Optional[str] = None
