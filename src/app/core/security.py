# src/app/core/security.py
import base64
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException, Request, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.app.core.config import config

from fastapi.responses import JSONResponse

security_basic = HTTPBasic()
security_bearer = HTTPBearer()


time = timedelta(hours=12)
key = config.SERV_KEYS
algorithm = 'HS256'


def criar_token(dados: dict):
    iat = datetime.now(timezone.utc)
    exp = datetime.now(timezone.utc) + time
    claims = dados.copy()
    claims.update({"iat": iat, "exp": exp})

    return jwt.encode(claims, key, algorithm)


def verificar_token(token: str):
    try:
        return jwt.decode(token, key, algorithm)
    except JWTError:
        return None


async def on_basic_auth(request: Request):
    basic = request.headers.get("authorization")
    if not basic:
        raise HTTPException(status_code=401, detail="Cabeçalho de autorização ausente")
    if not basic.lower().startswith("basic "):
        raise HTTPException(status_code=400, detail="Formato de autenticação inválido")
    try:
        encoded = basic.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return HTTPBasicCredentials(username=username, password=password)
    except Exception:
        raise HTTPException(status_code=400, detail="Basic malformado")


async def on_bearer_auth(credentials: HTTPAuthorizationCredentials = Security(security_bearer)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, key, algorithm)
        return payload  # ou dados de usuário decodificados
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido ou expirado",
        )


def on_basic_auth2(request: Request):
    basic = request.headers.get("authorization")
    if not basic:
        raise HTTPException(status_code=401, detail="Cabeçalho de autorização ausente")

    try:
        if basic.lower().startswith("basic"):
            encoded = basic.split(" ")[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
            return HTTPBasicCredentials(username=username, password=password)
        elif basic.lower().startswith("bearer"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Basic"},
            )

    except Exception:
        raise HTTPException(status_code=400, detail="Basic malformado")
