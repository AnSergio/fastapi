from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.app.core.websocket import manager
from src.app.core.security import verificar_token  # Função para validar Bearer Token (jwt.decode)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = None
    # Pega o protocolo do WebSocket (deve ser "Bearer", token)
    if websocket.headers.get("sec-websocket-protocol"):
        token = websocket.headers.get("sec-websocket-protocol", "").replace("Bearer, ", "")

    if not token:
        await websocket.close(code=1008)  # Policy Violation
        return

    # Valida o Token
    user = verificar_token(token)

    if not user:
        await websocket.close(code=4001)  # Policy Violation
        return

    # await websocket.accept()
    await manager.connect(websocket)
    print(f"🔑 Token válido: {user}")
    try:
        while True:
            await websocket.receive_text()  # Mantém a conexão viva (ping/pong)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
