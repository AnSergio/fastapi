from fastapi import APIRouter
from src.app.core.ws_manager import manager

router = APIRouter()


@router.get("/test")
async def test_websocket():
    await manager.send_message("📢 Mensagem de teste via WebSocket!")
    return {"status": "ok", "detail": "Mensagem enviada para todos os clientes WebSocket."}
