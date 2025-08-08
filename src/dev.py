# src/dev.py
import sys
import signal
import asyncio
import uvicorn
import threading
from src.app.main import app
from src.utils.realtime_fdb import main_fdb, stop_fdb
from src.utils.realtime_mdb import main_mdb, stop_mdb
from src.app.core.config import host, port, dns, user, password, uri


def start_fastapi():
    config_uvicorn = uvicorn.Config(app, host=host, port=port, reload=True)
    server = uvicorn.Server(config_uvicorn)
    server.run()


def start_watchers():
    print("⏳ Watchers em execução...")
    fdb_thread = threading.Thread(target=main_fdb, args=(dns, user, password), daemon=True)
    mdb_thread = threading.Thread(target=lambda: asyncio.run(main_mdb(uri)), daemon=True)
    fdb_thread.start()
    mdb_thread.start()
    return [fdb_thread, mdb_thread]


def main():
    # Threads
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

    start_watchers()

    def signal_handler(*_args):
        print(f"\n⛔ Recebido Ctrl+C! Encerrando serviços...")
        stop_fdb()
        stop_mdb()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Mantém o programa rodando enquanto o FastAPI estiver ativo
    try:
        while fastapi_thread.is_alive():
            fastapi_thread.join(timeout=1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
