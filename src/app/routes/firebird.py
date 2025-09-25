# src/routes/firebird.py
import fdb
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from src.app.schemas.firebird import FirebirdRequest
from src.utils.firebird import on_local, on_sql, on_options

router = APIRouter()


@router.post("/local")
async def on_fdb_local(body: FirebirdRequest):
    # print(f"body: {body}")
    sql: str
    params = body.params or []

    if body.local:
        try:
            sql = on_local(body.local, body.func, body.args)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao carregar SQL: {e}")

    options = on_options(body.host, body.db)

    try:
        con = fdb.connect(**options)
    except fdb.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão Firebird: {e}")

    try:
        is_modification = sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE"))

        if is_modification:
            # Operações de modificação (com transação)
            try:
                cur = con.cursor()
                cur.execute(sql, params)
                con.commit()
                return {"message": "Operação realizada com sucesso!"}
            except Exception as e:
                con.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao executar operação: {e}")
            finally:
                con.close()
        else:
            # SELECT — sem transação explícita
            try:
                cur = con.cursor()
                cur.execute(sql, params)
                columns = [desc[0].lower() for desc in cur.description]
                rows = cur.fetchall()

                transformed = []
                for row in rows:
                    transformed_row: Dict[str, Any] = {}
                    for col, val in zip(columns, row):
                        transformed_row[col] = val.strip() if isinstance(val, str) else val
                    transformed.append(transformed_row)

                return transformed
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao executar SELECT: {e}")
            finally:
                con.close()

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())


@router.post("/sql")
async def on_fdb_sql(body: FirebirdRequest):
    # print(f"body: {body}")
    sql: str
    params = body.params or []

    if not body.db:
        raise HTTPException(status_code=400, detail="Banco de dados é necessário!")
    if not body.local:
        raise HTTPException(status_code=400, detail="Arquivo SQL ou comando é necessário!")
    if body.local:
        try:
            sql = on_sql(body.local)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao carregar SQL: {e}")

    options = on_options(body.host, body.db)

    try:
        con = fdb.connect(**options)
    except fdb.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão Firebird: {e}")

    try:
        is_modification = sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE"))

        if is_modification:
            # Operações de modificação (com transação)
            try:
                cur = con.cursor()
                cur.execute(sql, params)
                con.commit()
                return {"message": "Operação realizada com sucesso!"}
            except Exception as e:
                con.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao executar operação: {e}")
            finally:
                con.close()
        else:
            # SELECT — sem transação explícita
            try:
                cur = con.cursor()
                cur.execute(sql, params)
                columns = [desc[0].lower() for desc in cur.description]
                rows = cur.fetchall()

                transformed = []
                for row in rows:
                    transformed_row: Dict[str, Any] = {}
                    for col, val in zip(columns, row):
                        transformed_row[col] = val.strip() if isinstance(val, str) else val
                    transformed.append(transformed_row)

                return transformed
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao executar SELECT: {e}")
            finally:
                con.close()

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())
