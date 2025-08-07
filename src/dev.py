# src/dev.py
import asyncio
import uvicorn
import threading
from src.utils.realtime_mdb import main as main_mdb, stop_watchers
from src.app.core.config import config


async def start_fastapi():
    config_uvicorn = uvicorn.Config("src.app.main:app", host=config.SERV_HOST, port=config.SERV_PORT, reload=True)
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


# Função que roda o watcher do MongoDB
def mongo_watcher():
    try:
        print("⏳ Processo paralelo rodando...")
        main_mdb(config.DB_URIS)
    except Exception as e:
        print("❌ Erro no watcher MongoDB:", e)


async def outro_processo():
    # Executa o watcher em thread separada
    thread = threading.Thread(target=mongo_watcher)
    thread.start()
    return thread


async def async_main():
    try:
        watcher_thread = await outro_processo()
        await asyncio.gather(start_fastapi())
    except asyncio.CancelledError:
        print("🧹 Tarefas canceladas")
        stop_watchers()
        if watcher_thread.is_alive():
            watcher_thread.join()
        print("✅ Finalizando com segurança...")


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("⛔ Encerrado pelo usuário (CTRL+C)")
