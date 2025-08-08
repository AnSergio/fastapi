# start.py
import asyncio
import uvicorn
import threading
from src.app.main import app
from src.utils.realtime_fdb import main_fdb, stop_fdb
from src.utils.realtime_mdb import main_mdb, stop_mdb
from src.app.core.config import config


async def start_fastapi():
    config_uvicorn = uvicorn.Config(
        app,
        host=config.SERV_HOST,
        port=config.SERV_PORT,
        reload=False,
        log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


def watchers_thread():
    print("⏳ Watchers em execução...")
    fdb_thread = threading.Thread(target=main_fdb, args=(config.DB_UDNS, config.DB_USER, config.DB_PASS))
    mdb_thread = threading.Thread(target=main_mdb, args=(config.DB_URIS,))
    fdb_thread.start()
    mdb_thread.start()
    fdb_thread.join()
    mdb_thread.join()


async def outro_processo():
    thread = threading.Thread(target=watchers_thread)
    thread.start()
    return thread


async def async_main():
    try:
        watcher_thread = await outro_processo()
        await asyncio.gather(start_fastapi())
    except asyncio.CancelledError:
        print("🧹 Limpando recursos...")
        stop_fdb()
        stop_mdb()
        if watcher_thread.is_alive():
            watcher_thread.join()


def main():
    try:
        run_main = asyncio.run(async_main())
    except KeyboardInterrupt:
        stop_fdb()
        stop_mdb()
        if run_main.watcher_thread.is_alive():
            run_main.watcher_thread.join()
        print("⛔ Encerrado pelo usuário")


if __name__ == "__main__":
    main()
