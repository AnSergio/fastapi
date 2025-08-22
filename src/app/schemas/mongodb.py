# src/app/schemas/mongodb.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AggregateRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    pipeline: List[Dict[str, Any]] = Field(..., description="Pipeline de agregação")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Opções adicionais para agregação")


class DeletesRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    query: Dict = Field(..., description="query")
    options: Optional[dict] = None


class FindsRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    filter: Dict = Field(..., description="filter")
    options: Optional[dict] = None


class FindReplaceRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    filter: Dict = Field(..., description="filter")
    replacement: Dict = Field(..., description="replace")
    options: Optional[dict] = None


class FindUpdateRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    filter: Dict = Field(..., description="filter")
    update: Dict = Field(..., description="update")
    options: Optional[dict] = None


class InsertRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    doc: Dict = Field(..., description="Documento a ser inserido")
    options: Optional[dict] = None


class InsertManyRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    docs: List[dict] = Field(..., description="docs")
    options: Optional[dict] = None


class UpdatesRequest(BaseModel):
    db: str = Field(..., description="Nome do banco de dados")
    coll: str = Field(..., description="Nome da coleção")
    query: Dict = Field(..., description="query")
    update: Dict = Field(..., description="update")
    options: Optional[dict] = None
