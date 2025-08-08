from fastapi import APIRouter
from src.app.core.websocket import manager


router = APIRouter()


@router.get("/test")
async def test_websocket():
    await manager.broadcast("realtime/firebird/cp_pedido")
    return {"status": "ok", "detail": "Mensagem enviada para todos os clientes WebSocket."}
