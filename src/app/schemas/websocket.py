# src/app/schemas/websocket.py
from pydantic import BaseModel


class WebSocketData(BaseModel):
    event: str
    message: str
