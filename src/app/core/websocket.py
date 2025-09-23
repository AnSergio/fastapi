# src/app/core/websocket.py
from fastapi import WebSocket
from typing import List, Any


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, subprotocol: str = None):
        await websocket.accept(subprotocol=subprotocol)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_to(self, websocket: WebSocket, message: Any):
        await websocket.send_json(message)

    async def send(self, message: Any):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)
                print("⚠️ WebSocket: broadcast disconnect", flush=True)


manager = ConnectionManager()
