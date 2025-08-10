# src/app/schemas/mongodb.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AggregateRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    pipeline: List[Dict[str, Any]] = Field(..., description="Pipeline de agregação")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Opções adicionais para agregação")


class DeleteRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    query: Dict = Field(..., alias="query")
    options: Optional[dict] = None


class FindRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    filter: Dict = Field(..., alias="filter")
    replacement: Optional[dict] = None
    update: Optional[dict] = None
    options: Optional[dict] = None


class InsertRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    doc: Optional[dict] = None
    docs: Optional[List[dict]] = None
    options: Optional[dict] = None


class UpdateRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    query: Dict = Field(..., alias="query")
    update: Optional[dict] = None
    options: Optional[dict] = None
