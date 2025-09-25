# src/utils/firebird.py
import os
import inspect
from importlib import util
from typing import Callable
from src.app.core.config import fdb_user, fdb_pass


local_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "local")
sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")
# print(f"🚀 Pasta Sql: {sql}")


def args_match(func_ref: Callable, *args, **kwargs):
    sig = inspect.signature(func_ref)
    params = list(sig.parameters.values())
    args_enviados = len(args)
    args_esperados = len(params)
    args_params = [str(p) for p in params]
    # print(f"args_match: args_enviados: {args_enviados}, args_esperados: {args_esperados}\n")

    if not args_enviados == args_esperados:
        raise TypeError(f"Consulata invalida, args_enviados: {args_enviados}, args_esperados: {args_esperados}, 'args': {args_params}")

    return


def on_local(local: str, func: str, args=None, kwargs=None) -> str:
    try:
        args = args or []
        kwargs = kwargs or {}

        path = os.path.join(local_dir, f"{local}.py")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Arquivo '{local}.py' não encontrado em {local_dir}")

        spec = util.spec_from_file_location(local, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível criar o spec para {local}.py")
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, func):
            raise AttributeError(f"Função '{func}' não encontrada no módulo '{local}'")

        func_ref = getattr(module, func)
        args_match(func_ref, *args, **kwargs)

        return func_ref(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"[on_local] Erro ao executar {local}.py, {func}: {e}")


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
        "user": fdb_user,
        "password": fdb_pass,
        "role": None,
    }


# sql = on_local("test", "usuario1", ["Sergio"])
# print(f"🚀 on_local: {sql}\n")


# except:
# raise FileNotFoundError(f"[on_local] Erro ao executar {local}.{func} com args={args}")
