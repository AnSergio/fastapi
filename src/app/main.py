# src/main.py
import asyncio
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from src.app.routes import test, websocket, auth, mongodb, pdftext
from src.app.core.security import on_bearer_auth
from src.utils.rate_limit import redis_url
from src.utils.realtime_fdb import main_fdb, stop_fdb
from src.utils.realtime_mdb import main_mdb, stop_mdb
from src.app.core.config import url, uri, dns, user, password, host, port
from src.app.core.websocket import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print(f"🌐 {app.title} em HTTP e WS http://{host}:{port} 🚀")
    task_redis = asyncio.create_task(redis_url(url))
    task_fdb = asyncio.create_task(main_fdb(dns, user, password, manager))
    task_mdb = asyncio.create_task(main_mdb(uri, manager))

    yield
    # shutdown
    print(f"🟥 {app.title} está finalizando!")
    stop_fdb()
    stop_mdb()
    for task in [task_redis, task_fdb, task_mdb]:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


# Cria app FastAPI
app = FastAPI(lifespan=lifespan, title="ApiRest FastAPI")


# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas organizadas
app.include_router(test.router)

app.include_router(websocket.router)

app.include_router(
    auth.router,
    prefix="/auth",
    dependencies=[Depends(RateLimiter(times=2, seconds=10))]
)

app.include_router(
    mongodb.router,
    prefix="/mongodb",
    tags=["MongoDB"],
    dependencies=[Depends(on_bearer_auth), Depends(RateLimiter(times=150, seconds=60))]
)

app.include_router(
    pdftext.router,
    prefix="/pdf",
    tags=["PDFs"],
    dependencies=[Depends(on_bearer_auth), Depends(RateLimiter(times=150, seconds=60))]
)

# print(f"🌐 Servidor HTTP e WS rodando http://{host}:{port} 🚀")
