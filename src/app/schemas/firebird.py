# src/app/schemas/firebird.py
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from src.app.core.config import fdb_host


class FirebirdRequest(BaseModel):
    host: Optional[str] = fdb_host
    db: str = Field(..., description="Banco de dados: /firebird/test.fdb")
    local: str = Field(..., description="Local do arquivo: test")
    func: Optional[str] = None
    args: Optional[List[Any]] = None
    params: Optional[List[Any]] = None
