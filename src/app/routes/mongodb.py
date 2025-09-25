# src/app/routes/mongodb.py
from fastapi import APIRouter,  HTTPException
from src.app.core.mongodb import convert_id,  convert_oid
from src.app.schemas.mongodb import AggregateRequest, DeleteRequest, FindReplaceRequest, FindUpdateRequest, FindRequest
from src.app.schemas.mongodb import InsertRequest, InsertManyRequest, UpdatesRequest
from src.app.core.config import client


router = APIRouter()


@router.post(
    "/aggregate",
    summary="Executa uma agregação no MongoDB",
    description="Recebe um pipeline de agregação e retorna os documentos resultantes"
)
async def on_aggregate(body: AggregateRequest):
    # print(f"body: {body}")
    pipeline = convert_oid(body.pipeline)
    options = body.options or {}

    if not body.db or not body.coll or not pipeline:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e pipeline são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        cursor = await collection.aggregate(pipeline, **options)
        result = []
        async for doc in cursor:
            doc = convert_id(doc)
            result.append(doc)

        if not result:
            raise HTTPException(status_code=401, detail="Aggregate não encontrado")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
async def on_delete(body: DeleteRequest):
    # print(f"body: {body}")
    query = convert_oid(body.query)
    options = body.options or {}

    if not body.db or not body.coll or not query:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e query são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.delete_one(query, **options)

        if not result.deleted_count:
            raise HTTPException(status_code=404, detail="Documento não encontrado para exclusão")

        return {"deleted_count": result.deleted_count}

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())


@router.delete("/deletemany")
async def on_delete_many(body: DeleteRequest):
    # print(f"body: {body}")
    query = convert_oid(body.query)
    options = body.options or {}

    if not body.db or not body.coll or not query:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e query são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.delete_many(query, **options)

        if not result.deleted_count:
            raise HTTPException(status_code=404, detail="Documentos não encontrado para exclusão")

        return {"deleted_count": result.deleted_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find")
async def on_find(body: FindRequest):
    # print(f"body: {body}")
    filter = convert_oid(body.filter)
    options = body.options or {}

    if not body.db or not body.coll:
        raise HTTPException(status_code=400, detail="Banco de dados e coleção são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        cursor = collection.find(filter, **options)

        result = []
        async for doc in cursor:
            doc = convert_id(doc)
            result.append(doc)

        if not result:
            return []

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/findone")
async def on_find_one(body: FindRequest):
    # print(f"body: {body}")
    filter = convert_oid(body.filter)
    options = body.options or {}

    if not body.db or not body.coll or not filter:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e filter são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.find_one(filter, **options)

        if not result:
            return {}

        result = convert_id(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finddelete")
async def on_find_one_and_delete(body: FindRequest):
    # print(f"body: {body}")
    filter = convert_oid(body.filter)
    options = body.options or {}

    if not body.db or not body.coll or not filter:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e filter são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.find_one_and_delete(filter, **options)

        if not result:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        result = convert_id(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/findreplace")
async def on_find_one_and_replace(body: FindReplaceRequest):
    # print(f"body: {body}")
    filter = convert_oid(body.filter)
    replacement = body.replacement
    options = body.options or {}

    if not body.db or not body.coll or not filter or not replacement:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção, filter e replacement são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.find_one_and_replace(filter, replacement, **options)

        if not result:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        result = convert_id(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/findupdate")
async def on_find_one_and_update(body: FindUpdateRequest):
    # print(f"body: {body}")
    filter = convert_oid(body.filter)
    update = body.update
    options = body.options or {}

    if not body.db or not body.coll or not filter or not update:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção, filter e update com $set são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.find_one_and_update(filter, update, **options)

        if not result:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        result = convert_id(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert")
async def on_insert_one(body: InsertRequest):
    # print(f"body: {body}")
    doc = body.doc
    options = body.options or {}

    if not body.db or not body.coll or not doc:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e doc são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.insert_one(doc, **options)

        inserted_id = str(result.inserted_id)
        return {"inserted_id": inserted_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insertmany")
async def on_insert_many(body: InsertManyRequest):
    # print(f"body: {body}")
    docs = body.docs
    options = body.options or {}

    if not body.db or not body.coll or not docs:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção e docs são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        cursor = await collection.insert_many(docs, **options)

        inserted_ids = [str(oid) for oid in cursor.inserted_ids]
        print(f"inserted_ids: {inserted_ids}")
        return {"inserted_ids": inserted_ids}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update")
async def on_update_one(body: UpdatesRequest):
    # print(f"body: {body}")
    query = convert_oid(body.query)
    update = body.update
    options = body.options or {}

    if not body.db or not body.coll or not query or not update:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção, query e update com $set são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.update_one(query, update, **options)

        if not result:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        return {"modified_count": result.modified_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/updatemany")
async def on_update_many(body: UpdatesRequest):
    # print(f"body: {body}")
    query = convert_oid(body.query)
    update = body.update
    options = body.options or {}

    if not body.db or not body.coll or not query or not update:
        raise HTTPException(status_code=400, detail="Banco de dados, coleção, query e update com $set são necessários!")

    try:
        db = client[body.db]
        collection = db[body.coll]
        result = await collection.update_many(query, update, **options)

        if not result:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        return {"modified_count": result.modified_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
