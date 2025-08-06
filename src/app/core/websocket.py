from typing import List
from fastapi import WebSocket
import asyncio


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept(subprotocol="Bearer")
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event: str, message: str):
        data = {"event": event, "message": message}
        for connection in self.active_connections:
            await connection.send_json(data)

    def broadcast_sync(self, event: str, message: str):
        # Para chamadas vindas de Thread (watcher)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast(event, message), loop)


manager = WebSocketManager()
