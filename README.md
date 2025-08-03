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
uv pip install -r requirements.txt

# Rodar com reload automático
uvicorn src.main:app --reload

uv run dev

.
├── src/
│   ├── main.py            # Ponto de entrada (FastAPI app)
│   ├── db/                # Conexão com o MongoDB (motor)
│   ├── models/            # Modelos de dados (Pydantic ou BSON)
│   ├── routes/            # Rotas organizadas por domínio
│   ├── utils/             # Funções auxiliares (ex: conversão de ObjectId)
│   └── config.py          # Configurações globais
├── tests/                 # Testes automatizados
├── pyproject.toml         # Configuração do projeto e dependências
├── README.md              # Este arquivo
└── .env                   # Variáveis de ambiente (opcional)

MONGO_URI=mongodb://localhost:27017
MONGO_DB=apirest

[tool.uv]
scripts = { dev = "uvicorn src.main:app --reload" }

```
