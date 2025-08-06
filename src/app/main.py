# src/main.py
import asyncio

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.core.security import on_bearer_auth
from src.app.core.realtime import on_realtime_fdb, on_realtime_mdb
from src.app.routes import websocket, auth, mongodb, task
from src.app.core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(on_realtime_fdb())
    # asyncio.create_task(on_realtime_mdb())
    yield

app = FastAPI(lifespan=lifespan, title="API REST em FastAPI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas organizadas
app.include_router(websocket.router)

app.include_router(auth.router, prefix="/auth")

app.include_router(mongodb.router, prefix="/mongodb", dependencies=[Depends(on_bearer_auth)])

app.include_router(task.router, prefix="/tasks")

realtime_mdb()


print(f"🌐 Servidor HTTP e WS rodando http://{config.SERV_HOST}:{config.SERV_PORT} 🚀")

# app.include_router(pdf.router, prefix="/pdf")
# app.include_router(comando.router, prefix="/comando")
# app.include_router(firebird.router, prefix="/firebird")
# @app.on_event("startup")
# async def startup_event():
#    watcher_thread = threading.Thread(target=realtime_mdb(config.DB_URIS),  daemon=True)
#    watcher_thread.start()
#    watcher_thread.join()
#    print("✅ MongoDB ChangeStream Monitor Started")

# stop_event = threading.Event()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#    thread = threading.Thread(target=realtime_mdb, daemon=True)
#    thread.start()
#
#    yield
#
#    stop_event.set()
#    thread.join()
