from fastapi import APIRouter,  HTTPException
from src.app.core.mongodb import convert_id, convert_oid
from src.app.schemas.mongodb import AggregateRequest
from src.app.core.config import client


router = APIRouter()


@router.post("/aggregate")
async def on_aggregate(body: AggregateRequest):
    # print(f"body: {body}")
    pipeline = convert_oid(body.pipeline)

    if not body.db or not body.coll or not pipeline:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e pipeline são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        cursor = collection.aggregate(pipeline, **(body.options or {}))

        resultado = []
        async for doc in cursor:
            doc = convert_id(doc)
            resultado.append(doc)

        if not resultado:
            raise HTTPException(status_code=401, detail="Aggregate não encontrado")
        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# print(f"body: {body}")
