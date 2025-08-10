from fastapi import APIRouter
from src.app.core.websocket import manager


router = APIRouter()


@router.get("/test")
async def test_ws():
    print(f"Test", flush=True)
    await manager.broadcast({"event": "teste", "user": "teste"})
    return {"status": "ok"}
