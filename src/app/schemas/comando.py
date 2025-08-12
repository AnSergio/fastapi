# src/app/schemas/comandos.py
from typing import Literal
from pydantic import BaseModel, Field


class ComandoLinuxRequest(BaseModel):
    nome: str = Field(..., description="Nome do comando")
    comando: Literal["start", "stop", "restart", "status"] = Field(..., description="start, stop, restart, status")


class ComandoWindowsRequest(BaseModel):
    comando: str = Field(..., description="Nome do comando")
