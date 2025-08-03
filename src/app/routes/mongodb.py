from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.app.core.config import config

router = APIRouter()

client = AsyncIOMotorClient(config.DB_URIS)


def validar_objectids(pipeline: List[dict]) -> bool:
    try:
        for stage in pipeline:
            for key, value in stage.items():
                if isinstance(value, dict) and "$match" in stage:
                    for k, v in value.get("$match", {}).items():
                        if k == "_id":
                            if isinstance(v, dict) and "$in" in v:
                                # Verifica lista de ObjectIds
                                for id_str in v["$in"]:
                                    ObjectId(id_str)
                            else:
                                ObjectId(v)
        return True
    except Exception:
        return False


def converter_objectid_pipeline(pipeline: list) -> list:
    for stage in pipeline:
        if "$match" in stage:
            match = stage["$match"]
            if "_id" in match:
                val = match["_id"]
                try:
                    # Se for string válida de ObjectId, converte
                    match["_id"] = ObjectId(val)
                except Exception:
                    # mantém como está se não for válido
                    pass
    return pipeline


class AggregateRequest(BaseModel):
    db: str
    coll: str
    pipeline: List[dict] = Field(..., alias="pipeline")
    options: Optional[dict] = None


@router.post("/aggregate")
async def on_aggregate(body: AggregateRequest):
    pipeline = converter_objectid_pipeline(body.pipeline)

    if not body.db or not body.coll or not pipeline:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e pipeline são necessários!")

    if not validar_objectids(pipeline):
        raise HTTPException(status_code=400, detail="IDs inválidos no pipeline!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        cursor = collection.aggregate(pipeline, **(body.options or {}))
        resultado = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # serializa ObjectId
            resultado.append(doc)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
