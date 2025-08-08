# 🚀 API REST - FastAPI + MongoDB + Motor

API assíncrona criada com [FastAPI](https://fastapi.tiangolo.com/) e [Motor](https://motor.readthedocs.io/)
(MongoDB async driver). Gerenciada com [uv](https://github.com/astral-sh/uv) para ambientes leves e modernos em Python.

---

## 📦 Requisitos

- Python 3.11+
- MongoDB 6+ (local ou remoto)
- [uv](https://github.com/astral-sh/uv) instalado globalmente:

```bash
pip install uv

# Instalar dependências
uv add

# Rodar com reload automático
uv run dev

.
├── src/
│   ├── app/                    # FastAPI
│   │    ├── core
│   │    │    ├── config.py     # Configurações globais
│   │    │    ├── mongodb.py    # Funções auxiliares (ex: conversão de ObjectId)
│   │    │    └── security.py
│   │    ├── models
│   │    ├── rotes              # Rotas organizadas por domínio
│   │    │    ├── auth.py
│   │    │    └── mongodb.py
│   │    ├── schemas
│   │    │    └── auth.py
│   │    └── main.py
│   └── dev.py
├── pyproject.toml              # Configuração do projeto e dependências
├── pyproject.toml              # Configuração do projeto e dependências
├── README.md                   # Este arquivo
└── .env                        # Variáveis de ambiente (opcional)

MONGO_URI=mongodb://localhost:27017
MONGO_DB=apirest

[tool.uv]
scripts = { dev = "uvicorn src.main:app --reload" }

```

```
Usando o pyinstaller

uv run pyinstaller --onefile --name apirest --add-data ".env:." start.py

```
