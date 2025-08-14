# src/utils/firebird.py
import os
import inspect
import traceback
import importlib.util
from typing import Any, Callable
from src.app.core.config import user, password


local_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "local")
sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")
# print(f"🚀 Pasta Sql: {sql}")


def verifica_args(func) -> int:
    sig = inspect.signature(func)
    obrigatorios = [
        p for p in sig.parameters.values()
        if p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    return len(obrigatorios)


def call_if_args_match(func_ref: Callable, *args) -> Any:
    sig = inspect.signature(func_ref)
    params = sig.parameters

    # Conta parâmetros obrigatórios (sem valor padrão)
    required_params = [
        p for p in params.values()
        if p.default is inspect.Parameter.empty and
        p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]

    if len(args) == len(required_params):
        return func_ref(*args)
    else:
        return ""


def on_local1(local: str, func: str, args=None) -> str:
    try:
        path = os.path.join(local_dir, f"{local}.py")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Arquivo '{local}.py' não encontrado em {local_dir}")

        spec = importlib.util.spec_from_file_location(local, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível criar o spec para {local}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, func):
            raise AttributeError(f"Função '{func}' não encontrada no módulo '{local}'")

        func_ref = getattr(module, func)

        sig = verifica_args(func_ref)

        if not sig or not args:
            print(f"🚀 not sig or not args: {sig, args}\n")
            return func_ref()
        elif sig or not args:
            print(f"🚀 sig or not args: {sig, args}\n")
            return FileNotFoundError(f"[on_local] Erro ao executar {local}.{func} falta args")

        return func_ref(*args)

    except:
        raise FileNotFoundError(f"[on_local] Erro ao executar {local}.{func} com args={args}")


def on_local(local: str, func: str, args=None) -> Any:
    try:
        path = os.path.join(local_dir, f"{local}.py")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Arquivo '{local}.py' não encontrado em {local_dir}")

        spec = importlib.util.spec_from_file_location(local, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível criar o spec para {local}.py")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, func):
            raise AttributeError(f"Função '{func}' não encontrada no módulo '{local}'")

        func_ref = getattr(module, func)

        obrigatorios = call_if_args_match(func_ref, args)
        print(f"🚀 Obrigatorios: {obrigatorios}\n")

        # Caso 1: função sem args obrigatórios
        if obrigatorios == "":

            return ""
            raise TypeError(f"A função '{func}' exige {obrigatorios} argumento(s) obrigatório(s)")

        return func_ref(*args)

    except Exception as e:
        raise RuntimeError(f"[on_local] Erro ao executar {local}.{func} com args={args}") from e


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


sql = on_local("test", "usuario")
print(f"🚀 Pasta Sql: {sql}\n")


# except:
# raise FileNotFoundError(f"[on_local] Erro ao executar {local}.{func} com args={args}")
