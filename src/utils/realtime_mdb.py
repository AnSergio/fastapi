# src/utils/realtime_mdb.py
import asyncio
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError
from src.app.core.websocket import ConnectionManager


stop_event = asyncio.Event()
client: AsyncMongoClient | None = None


def stop_mdb():
    stop_event.set()


async def start_mdb(uri: str, manager: ConnectionManager):
    global client
    time_delay = 1
    valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}

    while not stop_event.is_set():
        print(f"📡 Iniciando realtime_mdb! (delay: {time_delay}s)", flush=True)

        try:
            client = AsyncMongoClient(uri)
            tasks = []
            time_delay = 1  # reset do backoff

            async def watch_change(client: AsyncMongoClient):
                change_stream = await client.watch()
                try:
                    async for change in change_stream:
                        ns = change.get("ns")
                        if ns:
                            realtime = f"{ns['db']}/{ns['coll']}"
                            await manager.send({"event": "realtime", "message": realtime})
                            # print(realtime, flush=True)

                        if stop_event.is_set():
                            break
                finally:
                    await change_stream.close()

            tasks.append(asyncio.create_task(watch_change(client)))
            await asyncio.gather(*tasks)

        except asyncio.CancelledError:
            tasks.clear()
            break

        except PyMongoError as e:
            print(f"❌ MDB Erro geral: {e}", flush=True)
            time_delay = valid_time.get(time_delay, 60)
            print(f"🔄 Reiniciando MongoDB em {time_delay}s...\n", flush=True)
            await asyncio.sleep(time_delay)

        finally:
            if client:
                client.close()

    # print("🛑 Watcher realtime_mdb finalizado!", flush=True)


async def main_mdb(uri: str, manager: ConnectionManager):
    global stop_event
    stop_event.clear()
    task = asyncio.create_task(start_mdb(uri, manager))
    try:
        await stop_event.wait()
        task.cancel()
        await task
    except asyncio.CancelledError:
        task.cancel()
        await task
    finally:
        print("✅ MDB Watcher finalizado")
