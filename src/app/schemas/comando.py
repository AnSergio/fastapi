# src/app/schemas/comandos.py
from pydantic import BaseModel, Field


class ComandoLinuxRequest(BaseModel):
    nome: str = Field(..., description="Nome do comando")
    comando: str = Field(..., description="start, stop, restart, status")


class ComandoWindowsRequest(BaseModel):
    comando: str = Field(..., description="Nome do comando")
