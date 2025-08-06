# src/app/config.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

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

pymongo_client = MongoClient(config.DB_URIS)
