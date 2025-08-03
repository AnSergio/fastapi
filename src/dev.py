# src/dev.py
from src.app.core.config import config
import uvicorn


def main():
    uvicorn.run(
        "src.app.main:app",
        host=config.SERV_HOST,
        port=config.SERV_PORT,
        reload=True
    )
