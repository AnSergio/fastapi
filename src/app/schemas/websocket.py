# src/app/schemas/websocket.py
from pydantic import BaseModel


class WebSocketData(BaseModel):
    event: str
    message: str


class WebSocketUser(BaseModel):
    _id: str
    nome: str
    iat: int
    exp: int
