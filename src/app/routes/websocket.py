from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from src.app.core.websocket import manager
from src.app.core.security import verificar_token  # Função para validar Bearer Token (jwt.decode)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = None
    # Pega o protocolo do WebSocket (deve ser "Bearer", token)
    if websocket.headers.get("sec-websocket-protocol"):
        protocols = websocket.headers.get("sec-websocket-protocol").split(",")
        if len(protocols) >= 2 and protocols[0].strip() == "Bearer":
            token = protocols[1].strip()

    if not token:
        await websocket.close(code=1008)  # Policy Violation
        return

    # Valida o Token
    try:
        payload = verificar_token(token)
        print(f"🔑 Token válido: {payload}")
    except Exception:
        await websocket.close(code=4001)  # Custom code for Invalid Token
        return

    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantém a conexão viva (ping/pong)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
