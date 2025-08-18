# src/app/config.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()


class Config:
    # Servidor
    host = os.getenv("SERV_HOST", "127.0.0.1")
    port = int(os.getenv("SERV_PORT", "8000"))
    nome = os.getenv("SERV_NAME", "Teste")
    key = os.getenv("SERV_KEY", "supersecret")
    # Redis
    rdb_url = os.getenv("RDB_URL", "redis://127.0.0.1:6379")
    # MongoDB
    mdb_uri = os.getenv("MDB_URI", "mongodb://teste:teste@127.0.0.1:27017/")
    # firebird
    fdb_dns = os.getenv("FDB_DNS", "127.0.0.1:/home/firebird/dados.fdb")
    fdb_host = os.getenv("FDB_PASS", "127.0.0.1:/home/firebird/dados.fdb")
    fdb_user = os.getenv("FDB_USER", "SYSDBA")
    fdb_pass = os.getenv("FDB_PASS", "masterkey")


config = Config()

# Servidor
host = config.host
port = config.port
nome = config.nome
key = config.key
# Redis
rdb_url = config.rdb_url
# MongoDB
mdb_uri = config.mdb_uri
# firebird
fdb_dns = config.fdb_dns
fdb_host = config.fdb_host
fdb_user = config.fdb_user
fdb_pass = config.fdb_pass


client = AsyncIOMotorClient(mdb_uri)
