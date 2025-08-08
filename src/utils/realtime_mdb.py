# src/utils/realtime_mdb.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Bancos que não serão monitorados
dbs_ignorados = {"admin", "config", "local"}

# Retry progressivo (em segundos)
valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}

# Controle externo
stop_event = asyncio.Event()


def stop_mdb():
    stop_event.set()


async def start_watcher(uri: str, time_delay: int):
    client = AsyncIOMotorClient(uri)

    async def on_restart():
        nonlocal time_delay
        time_delay = valid_time.get(time_delay, 60)
        stop_event.set()

    async def on_change(change_stream):
        async for change in change_stream:
            ns = change.get("ns")
            if ns:
                realtime = f"{ns['db']}/{ns['coll']}"
                print(f"realtime/{realtime}", flush=True)
                # await manager.broadcast(f"realtime/{realtime}")

            if stop_event.is_set():
                await change_stream.close()
                break

    try:
        dbs_info = await client.admin.command("listDatabases")
        databases = dbs_info["databases"]
        time_delay = 1
        tasks = []

        for db_info in databases:
            db_name = db_info["name"]
            if db_name in dbs_ignorados:
                continue

            db = client[db_name]
            colls = await db.list_collection_names()
            for coll_name in colls:
                collection = db[coll_name]
                change_stream = collection.watch()
                tasks.append(asyncio.create_task(on_change(change_stream)))

        # Aguarda todas as tasks terminarem (ou o stop_event ser ativado)
        await asyncio.gather(*tasks)

    except asyncio.CancelledError:
        print("🛑 Interrompido manualmente", flush=True)
        raise
    except Exception as e:
        if not stop_event.is_set():
            print(f"❌ Erro geral: {e}", flush=True)
            await on_restart()
        else:
            client.close()


async def main_mdb(uri: str):
    global stop_event
    time_delay = 1

    while not stop_event.is_set():
        stop_event.clear()

        print(f"📡 Iniciando realtime_mdb! (delay: {time_delay}s)", flush=True)
        task = asyncio.create_task(start_watcher(uri, time_delay))

        try:
            await task
        except asyncio.CancelledError:
            print("🛑 Watcher cancelado", flush=True)

        if stop_event.is_set():
            break

        print(f"🔄 Reiniciando MongoDB em {time_delay}s...\n", flush=True)
        await asyncio.sleep(time_delay)

    print("🛑 Watcher realtime_mdb finalizado!", flush=True)
