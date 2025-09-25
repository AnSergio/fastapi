# src/app/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.app.core.websocket import manager


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008, reason="Token não fornecido")
        return

    try:
        await manager.connect(websocket)
        await manager.send({"event": "connection", "message": f"{token} connected"})
        print(f"✅ Conectado: {token}", flush=True)

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                # resposta direta ao remetente
                await manager.send_to(websocket, "pong")
                # print(f"🚀 Recebendo de {token}: {data}", flush=True)

            # send para todos
            # await manager.send("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send({"event": "connection", "message": f"{token} disconnected"})
        print(f"❌ Desconectado: {token}", flush=True)
