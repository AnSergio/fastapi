from fastapi import APIRouter
# from src.app.routes.socketio import sio

router = APIRouter()


@router.get("/test")
async def test_ws():
    # await sio.emit("realtime", "acesso/usuarios")
    return {"status": "ok"}
