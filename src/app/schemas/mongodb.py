from typing import List, Optional
from pydantic import BaseModel, Field


class AggregateRequest(BaseModel):
    db: str
    coll: str
    pipeline: List[dict] = Field(..., alias="pipeline")
    options: Optional[dict] = None
