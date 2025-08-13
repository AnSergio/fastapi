# src/utils/firebird.py
import os
import importlib.util
from src.app.core.config import user, password

local_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "local")
sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")
# print(f"🚀 Pasta Sql: {sql}")


def on_local(local: str, func: str, args=None) -> str:
    try:
        path = os.path.join(local_dir, f"{local}.py")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Arquivo '{local}.py' não encontrado em {local_dir}")

        spec = importlib.util.spec_from_file_location(local, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, func):
            raise AttributeError(f"Função '{func}' não encontrada no módulo '{local}'")

        func_ref = getattr(module, func)
        args = args or []
        return func_ref(*args)
    except:
        raise FileNotFoundError(f"[on_local] Erro ao executar {local}.{func} com args={args}")


def on_sql(local: str) -> str:
    try:
        path = os.path.join(sql_dir, f"{local}.sql")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Arquivo SQL '{local}' não encontrado em {sql_dir}")
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()
            return sql
    except:
        raise FileNotFoundError(f"[on_local] Erro ao executar {local}")


def on_options(host: str, db: str):
    return {
        "host": host,
        "port": 3050,
        "database": db,
        "user": user,
        "password": password,
        "role": None,
    }


# sql = on_local("test", "usuario", ["ansergio"])
# print(f"🚀 Pasta Sql: {sql}")
