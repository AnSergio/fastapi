# src/app/schemas/pdftext.py
from typing import Optional
from pydantic import BaseModel, Field


class PdfTextRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    base64: str = Field(..., description="Base64 do Pdf")
    encod: Optional[str] = None
