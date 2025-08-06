# src/app/routes/auth.py
import base64
import secrets
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.app.core.mongodb import convert_id
from src.app.core.security import criar_token, on_basic_auth
from src.app.core.config import client
from src.app.schemas.auth import AuthResponse, description, responses


router = APIRouter()
security = HTTPBasic()


@router.get(
    "/",
    tags=["Autenticação"],
    summary="Autenticar usuário",
    description=description,
    response_model=AuthResponse,
    responses=responses,
    status_code=200
)
async def auth(credentials: HTTPBasicCredentials = Depends(on_basic_auth)):
    if not (credentials.username and credentials.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    pipeline = [
        {"$match": {"nome": credentials.username}},
        {"$lookup": {"from": "rotas", "localField": "perfil", "foreignField": "nome", "as": "rota"}},
        {"$unwind": {"path": "$rota", "preserveNullAndEmptyArrays": True}},
        {"$project": {"_id": 1, "nome": 1, "senha": 1, "perfil": 1, "nivel": 1, "status": 1, "venda": 1, "imagem": 1, "rotas": "$rota.rotas"}}
    ]

    try:
        db = client["acesso"]
        collection = db["usuarios"]
        cursor = collection.aggregate(pipeline)

        doc = await anext(cursor, None)
        if not doc:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        password = base64.b64decode(doc["senha"]).decode("utf-8")
        valida = secrets.compare_digest(credentials.password, password)

        if not (valida):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        doc = convert_id(doc)
        # print(f"doc: {doc}")

        token = criar_token({"_id": str(doc["_id"]), "user": credentials.username})

        usuario = {
            "_id": str(doc["_id"]),
            "nome": doc["nome"],
            "perfil": doc["perfil"],
            "nivel": int(doc["nivel"]),
            "status": doc["status"],
            "venda": doc.get("venda", ""),
            "imagem": doc.get("imagem", "")
        }

        return {"token": token, "usuario": usuario, "rotas": doc.get("rotas", [])}

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())


# print(f"credentials: {credentials}")
