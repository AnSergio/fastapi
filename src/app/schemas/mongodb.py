from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AggregateRequest(BaseModel):
    db: str
    coll: str
    pipeline: List[dict] = Field(..., alias="pipeline")
    options: Optional[dict] = None


class DeleteRequest(BaseModel):
    db: str
    coll: str
    query: Dict = Field(..., alias="query")
    options: Optional[dict] = None


class FindRequest(BaseModel):
    db: str
    coll: str
    filter: Dict = Field(..., alias="filter")
    replacement: Optional[dict] = None
    update: Optional[dict] = None
    options: Optional[dict] = None


class InsertRequest(BaseModel):
    db: str
    coll: str
    doc: Optional[dict] = None
    docs: Optional[List[dict]] = None
    options: Optional[dict] = None


class UpdateRequest(BaseModel):
    db: str
    coll: str
    query: Dict = Field(..., alias="query")
    update: Optional[dict] = None
    options: Optional[dict] = None
