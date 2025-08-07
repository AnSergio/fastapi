# src/app/core/ws_manager.py
from typing import List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # <- Remova subprotocol
        self.active_connections.append(websocket)
        print(f"🔌 Conexões ativas: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        print(f"💬 Enviando para {len(self.active_connections)} conexões...")
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"❌ Erro ao enviar: {e}")


manager = ConnectionManager()
