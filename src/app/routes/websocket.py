# src/app/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.app.core.security import verificar_token
from src.app.core.websocket import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = None
    # Extrai o protocolo e token do cabeçalho
    if websocket.headers.get("sec-websocket-protocol"):
        token = websocket.headers.get("sec-websocket-protocol", "").replace("Bearer, ", "")

    if not token:
        await websocket.close(code=1008)
        return

    # Valida o Token JWT
    user = verificar_token(token)

    if not user:
        await websocket.close(code=4001)
        return

    # Aceita conexão com o mesmo subprotocol enviado
    try:
        await manager.connect(websocket)
        print(f"Client: {user}")
        await manager.broadcast(f"Client: {user}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("❌ Cliente desconectado")
