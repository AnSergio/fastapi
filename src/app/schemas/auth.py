# src/app/schemas/auth.py
from pydantic import BaseModel, Field
from typing import List, Optional


class Usuario(BaseModel):
    id: str = Field(..., alias="_id")
    nome: str
    perfil: str
    nivel: int
    status: bool
    venda: Optional[str] = ""
    imagem: Optional[str] = ""


class ChildRoute(BaseModel):
    path: str


class Rota(BaseModel):
    path: str
    children: Optional[List[ChildRoute]] = []


class AuthResponse(BaseModel):
    token: str
    usuario: Usuario
    rotas: List[Rota]


description = "Autentica um usuário via HTTP Basic e retorna token e dados do usuário"

responses = {
    200: {
        "description": "Login bem-sucedido. Retorna token, dados do usuário e rotas.",
        "content": {
            "application/json": {
                "example": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "usuario": {
                        "_id": "68684c9dca1c22496e69ded8",
                        "nome": "Teste",
                        "perfil": "Iniciante",
                        "nivel": "1",
                        "status": True,
                        "venda": "",
                        "imagem": ""
                    },
                    "rotas": [
                        {
                            "path": "/acesso",
                            "children": [
                                {"path": "usuario"}
                            ]
                        }
                    ]
                }
            }
        },
    },
    401: {
        "description": "Credenciais inválidas ou usuário não encontrado.",
        "content": {
            "application/json": {
                "examples": {
                    "Credenciais inválidas": {
                        "value": {"detail": "Credenciais inválidas"}
                    },
                    "Usuário não encontrado": {
                        "value": {"detail": "Usuário não encontrado"}
                    },
                    "Formato inválido": {
                        "value": {"detail": "Formato de autenticação inválido"}
                    }
                }
            }
        }
    },
    500: {
        "description": "Erro interno do servidor.",
        "content": {
            "application/json": {
                "example": {"detail": "Internal Server Error"}
            }
        }
    }
}
