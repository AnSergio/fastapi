# src/utils/realtime_mdb.py
# import os
# import psutil
import asyncio
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from src.app.core.websocket import ConnectionManager

stop_event = asyncio.Event()
# process = psutil.Process(os.getpid())
client = None


def stop_mdb():
    stop_event.set()
    # process.terminate()


async def start_watcher(uri: str, manager: ConnectionManager):
    global client
    time_delay = 1
    valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
    dbs_ignorados = {"admin", "config", "local"}

    while not stop_event.is_set():
        print(f"📡 Iniciando realtime_mdb! (delay: {time_delay}s)", flush=True)

        try:
            client = AsyncIOMotorClient(uri)
            dbs_info = await client.admin.command("listDatabases")
            databases = dbs_info["databases"]
            tasks_watch = []
            time_delay = 1

            async def watch_collection(collection: AsyncIOMotorCollection):
                try:
                    async with collection.watch() as change_stream:
                        async for change in change_stream:
                            ns = change.get("ns")
                            if ns:
                                realtime = f"{ns['db']}/{ns['coll']}"
                                # print(realtime, flush=True)
                                await manager.broadcast({"event": "realtime", "message": realtime})

                            if stop_event.is_set():
                                break
                except:
                    pass

            for db_info in databases:
                db_name = db_info["name"]
                if db_name in dbs_ignorados:
                    continue

                db = client[db_name]
                colls = await db.list_collection_names()
                for coll_name in colls:
                    collection = db[coll_name]
                    tasks_watch.append(asyncio.create_task(watch_collection(collection)))

            await asyncio.gather(*tasks_watch)

        except asyncio.CancelledError:
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

    try:
        task = asyncio.create_task(start_watcher(uri, manager))
        await stop_event.wait()
        print("🛑 MDB Sinal de parada recebido")
        task.cancel()
        await task
    except asyncio.CancelledError:
        pass
    finally:
        print("✅ MDB Watcher finalizado")
