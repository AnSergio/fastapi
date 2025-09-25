# src/app/core/security.py
import base64
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.app.core.config import key, song_key


security_basic = HTTPBasic()
security_bearer = HTTPBearer()

time = timedelta(hours=12)
algorithms = 'HS256'


def criar_token(dados: dict):
    iat = datetime.now(timezone.utc)
    exp = datetime.now(timezone.utc) + time
    claims = dados.copy()
    claims.update({"iat": iat, "exp": exp})

    return jwt.encode(claims, key, algorithms)


def verificar_token(token: str):
    try:
        return jwt.decode(token, key, algorithms)
    except JWTError as e:
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


async def on_basic_songs(request: Request):
    basic = request.headers.get("authorization")
    token = None

    if basic and basic.lower().startswith("basic "):
        encoded = basic.split(" ")[1]
        token = base64.b64decode(encoded).decode("utf-8").replace(":", "")

    else:
        token = request.query_params.get("token")

    try:
        if not token:
            raise HTTPException(status_code=401, detail="Token não encontrado")

        if token != song_key:
            raise HTTPException(status_code=401, detail="Token inválido")

        return token

    except Exception:
        raise HTTPException(status_code=400, detail="Basic malformado")


def on_bearer_auth(request: Request):
    bearer = request.headers.get("authorization")
    token = None

    # tenta pegar do header
    if bearer and bearer.lower().startswith("bearer "):
        token = bearer.split(" ")[1]
    else:
        # tenta pegar da query
        token = request.query_params.get("token")

    if not token:
        raise HTTPException(status_code=401, detail="Token não encontrado")

    try:
        payload = jwt.decode(token, key, algorithms)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido ou expirado",
        )
