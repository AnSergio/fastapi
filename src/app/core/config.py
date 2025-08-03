# src/app/config.py
import os
from bson import ObjectId
from fastapi import HTTPException
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()


class Config:
    SERV_HOST = os.getenv("SERV_HOST", "127.0.0.1")
    SERV_PORT = int(os.getenv("SERV_PORT", "3300"))
    SERV_NAME = os.getenv("SERV_NAME", "Teste")
    SERV_KEYS = os.getenv("SERV_KEYS", "supersecret")
    DB_URIS = os.getenv("DB_URIS", "mongodb://teste:teste@127.0.0.1:27017/")
    DB_USER = os.getenv("DB_USER", "sysdba")
    DB_PASS = os.getenv("DB_PASS", "masterkey")


config = Config()


client = AsyncIOMotorClient(config.DB_URIS)


def normalize_object_id(doc: dict) -> dict:
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def normalize_object_ids(docs: list[dict]) -> list[dict]:
    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return docs


def ensure_object_id(filter: dict) -> dict:
    if "_id" in filter:
        _id = filter["_id"]
        try:
            # Se vier como {"$oid": "..."} do JSON, extrai
            if isinstance(_id, dict) and "$oid" in _id:
                _id = _id["$oid"]

            filter["_id"] = ObjectId(str(_id))
        except Exception:
            raise HTTPException(status_code=400, detail="ID inválido!")
    return filter


def ensure_object_ids(filters: list[dict]) -> list[dict]:
    for filter in filters:
        if "_id" in filter:
            try:
                _id = filter["_id"]
                if isinstance(_id, dict) and "$oid" in _id:
                    _id = _id["$oid"]
                filter["_id"] = ObjectId(str(_id))
            except Exception:
                raise HTTPException(status_code=400, detail="ID inválido!")

        if "$match" in filter and "_id" in filter["$match"]:
            try:
                _id = filter["$match"]["_id"]
                if isinstance(_id, dict) and "$oid" in _id:
                    _id = _id["$oid"]
                filter["$match"]["_id"] = ObjectId(str(_id))
            except Exception:
                raise HTTPException(status_code=400, detail="ID inválido!")

    return filters
