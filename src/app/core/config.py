# src/app/config.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

load_dotenv()


class Config:
    host = os.getenv("SERV_HOST", "127.0.0.1")
    port = int(os.getenv("SERV_PORT", "8000"))
    nome = os.getenv("SERV_NAME", "Teste")
    key = os.getenv("SERV_KEYS", "supersecret")
    url = os.getenv("DB_URLS", "redis://127.0.0.1:6379")
    uri = os.getenv("DB_URIS", "mongodb://teste:teste@127.0.0.1:27017/")
    dns = os.getenv("DB_UDNS", "127.0.0.1:/home/firebird/dados.fdb")
    user = os.getenv("DB_USER", "SYSDBA")
    password = os.getenv("DB_PASS", "masterkey")


config = Config()


host = config.host
port = config.port
nome = config.nome
key = config.key
url = config.url
uri = config.uri
dns = config.dns
user = config.user
password = config.password


client = AsyncIOMotorClient(uri)

pymongo_client = MongoClient(uri)
