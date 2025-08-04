# src/main.py
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.core.security import on_bearer_auth
from src.app.routes import auth, mongodb, task

from src.app.core.config import config

app = FastAPI(title="API REST em FastAPI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas organizadas
app.include_router(auth.router, prefix="/auth")

app.include_router(mongodb.router, prefix="/mongodb", dependencies=[Depends(on_bearer_auth)])

app.include_router(task.router, prefix="/tasks")

print(f"🌐 Servidor HTTP e WS rodando http://{config.SERV_HOST}:{config.SERV_PORT} 🚀")

# app.include_router(pdf.router, prefix="/pdf")
# app.include_router(comando.router, prefix="/comando")
# app.include_router(firebird.router, prefix="/firebird")
