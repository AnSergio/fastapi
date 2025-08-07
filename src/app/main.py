# src/main.py
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.core.security import on_bearer_auth
from src.app.routes import test, websocket, auth, mongodb
from src.app.core.config import config


app = FastAPI(title="API REST FastAPI")

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

app.include_router(test.router)

app.include_router(auth.router, prefix="/auth")

app.include_router(mongodb.router, prefix="/mongodb", tags=["MongoDB"], dependencies=[Depends(on_bearer_auth)])

print(f"🌐 Servidor HTTP e WS rodando http://{config.SERV_HOST}:{config.SERV_PORT} 🚀")
