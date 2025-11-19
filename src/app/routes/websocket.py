# src/app/routes/websocket.py
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.app.core.websocket import manager
from src.app.core.security import verificar_token
from src.app.schemas.websocket import WebSocketData, WebSocketUser

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008, reason="Token não fornecido")
        return

    try:
        usuario = verificar_token(token)
        if not usuario:
            await websocket.close(code=1008, reason="Token inválido ou expirado")
            return

        user = WebSocketUser(**usuario)
        await manager.connect(websocket)
        await manager.send({"event": "connection", "message": f"{user.nome} connected"})
        print(f"✅ Conectado: {user.nome}", flush=True)

        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            receiver = WebSocketData(**data_json)
            # print(f"🚀 receiver {receiver}", flush=True)

            if receiver.event == "ping":
                # resposta direta ao remetente
                await manager.send_to(websocket, {"event": "pong", "message": f"{user.nome}"})
                # print(f"🚀 Manager {data}", flush=True)

            # send para todos
            # await manager.send("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send({"event": "connection", "message": f"{token} disconnected"})
        print(f"❌ Desconectado: {token}", flush=True)
