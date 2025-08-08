# src/utils/realtime_mdb.py
import time
import threading
from pymongo import MongoClient
from pymongo.errors import PyMongoError, OperationFailure


# Intervalos de retry progressivos (em segundos)
valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
initial_time = 1
is_client_closed = False

# Bancos que não serão monitorados
dbs_ignorados = ["admin", "config", "local"]

# Guarda os streams ativos para poder fechá-los depois (simulado via flags)
active_threads = []
stop_event = threading.Event()


def stop_mdb():
    stop_event.set()


def start_watchers(uri, time_delay):
    client = MongoClient(uri)
    admin = client.admin

    def on_restart():
        nonlocal time_delay
        time_delay = valid_time[time_delay]
        stop_event.set()

    try:
        dbs_info = admin.command("listDatabases")["databases"]
        time_delay = 1  # Reset tempo a cada início bem-sucedido

        for db_info in dbs_info:
            db_name = db_info["name"]
            if db_name in dbs_ignorados:
                continue

            db = client[db_name]
            for coll_name in db.list_collection_names():
                coll = db[coll_name]
                thread = threading.Thread(
                    target=watch_coll,
                    args=(coll, db_name, coll_name, on_restart),
                    daemon=True
                )
                thread.start()
                active_threads.append(thread)

        # Aguardar enquanto não houver pedido de reinício
        while not stop_event.is_set():
            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Interrompido manualmente", flush=True)
        raise
    except Exception as e:
        print(f"❌ Erro geral: {e}", flush=True)
        on_restart()
    finally:
        client.close()
        print("✅ Cliente Mongo encerrado com segurança", flush=True)


def watch_coll(coll, db_name, coll_name, on_restart):
    try:
        with coll.watch() as change_stream:
            for change in change_stream:
                if stop_event.is_set():
                    break
                ns = change.get("ns")
                if ns:
                    realtime = f"{ns['db']}/{ns['coll']}"
                    print(f"realtime/{realtime}", flush=True)

    except (OperationFailure, PyMongoError) as e:
        print(f"❌ Erro em {db_name}/{coll_name}: {e}", flush=True)
        on_restart()


def main_mdb(uri):
    global active_threads
    time_delay = initial_time

    while not stop_event.is_set():
        stop_event.clear()
        active_threads = []

        print(f"📡 Iniciando realtime_mdb! (delay: {time_delay}s)", flush=True)
        start_watchers(uri, time_delay)

        if stop_event.is_set():
            break

        print(f"Reiniciando em {time_delay}s...\n", flush=True)
        time.sleep(time_delay)

    print("🛑 Watcher realtime_mdb finalizado!", flush=True)
