# src/dev.py
import asyncio
import uvicorn
import threading
from src.utils.realtime_fdb import main_fdb, stop_fdb
from src.utils.realtime_mdb import main_mdb, stop_mdb
from src.app.core.config import config


async def start_fastapi():
    config_uvicorn = uvicorn.Config("src.app.main:app", host=config.SERV_HOST, port=config.SERV_PORT, reload=True)
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


# Função que roda os watchers (MongoDB + Firebird) em paralelo
def watchers_thread():
    try:
        print("⏳ Processo paralelo rodando...")

        # Threads separadas para MongoDB e Firebird
        fdb_thread = threading.Thread(target=main_fdb, args=(config.DB_UDNS, config.DB_USER, config.DB_PASS))
        mdb_thread = threading.Thread(target=main_mdb, args=(config.DB_URIS,))

        fdb_thread.start()
        mdb_thread.start()

        fdb_thread.join()
        mdb_thread.join()

    except Exception as e:
        print("❌ Erro nos watchers:", e)


async def outro_processo():
    # Roda os watchers em thread separada para não travar o loop principal
    thread = threading.Thread(target=watchers_thread)
    thread.start()
    return thread


async def async_main():
    try:
        watcher_thread = await outro_processo()
        await asyncio.gather(start_fastapi())

    except asyncio.CancelledError:
        print("🧹 Tarefas canceladas")
        stop_fdb()
        stop_mdb()
        if watcher_thread.is_alive():
            watcher_thread.join()
        print("✅ Finalizando com segurança...")


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("⛔ Encerrado pelo usuário (CTRL+C)")
