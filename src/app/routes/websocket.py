# src/app/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.app.core.security import verificar_token
from src.app.core.websocket import manager

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    # Extrai o token do subprotocol
    raw_protocol = websocket.headers.get("sec-websocket-protocol", "")
    token = raw_protocol.replace("Bearer, ", "").strip()

    if not token:
        await websocket.close(code=1008, reason="Token não fornecido")
        return

    # Valida token JWT
    user = verificar_token(token)
    if not user:
        await websocket.close(code=4001, reason="Token inválido ou expirado")
        return

    # Conecta cliente
    try:
        await manager.connect(websocket, subprotocol="Bearer")
        print(f"✅ Conectado: {user}", flush=True)

        while True:
            await websocket.receive_text()
            # print(f"✅ Conectado: {user}", flush=True)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"event": "user_disconnected", "_id": user["_id"], "nome": user["nome"]})
