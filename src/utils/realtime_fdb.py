# src/utils/realtime_fdb.py
import asyncio
from fdb import connect, Connection, Error
from src.app.core.websocket import ConnectionManager


stop_event = asyncio.Event()
client: Connection | None = None


def stop_fdb():
    stop_event.set()


async def start_fdb(dsn: str, user: str, password: str, manager: ConnectionManager):
    global client
    time_delay = 1
    valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
    event_nomes = ["cp_pedido", "cp_pedido_item", "tnfcanfen", "tnfcanfsa", "tnfitnfen", "tnfitnfsa"]

    while not stop_event.is_set():
        print(f"📡 Iniciando realtime_fdb! (delay: {time_delay}s)", flush=True)

        try:
            client = connect(dsn=dsn, user=user, password=password)
            tasks = []
            time_delay = 1

            async def watch_post(client: Connection):
                eventos = None
                try:
                    while not stop_event.is_set():
                        eventos = client.event_conduit(event_nomes)
                        eventos.begin()
                        tasks_event = await asyncio.to_thread(eventos.wait, 1)
                        eventos.close()
                        for nome, event in tasks_event.items():
                            if event > 0:
                                realtime = f"firebird/{nome}"
                                await manager.broadcast({"event": "realtime", "message": realtime})
                                print(realtime, flush=True)

                except:
                    tasks_event.clear()
                    eventos.close()
                    eventos = None

            tasks.append(asyncio.create_task(watch_post(client)))
            await asyncio.gather(*tasks)

        except asyncio.CancelledError:
            tasks.clear()
            break

        except Error as e:
            print(f"❌ FDB Erro geral: {e}", flush=True)
            time_delay = valid_time.get(time_delay, 60)
            print(f"🔄 Reiniciando Firebird em {time_delay}s...\n", flush=True)
            await asyncio.sleep(time_delay)

        finally:
            if client and not client.closed:
                client.close()

    # print("🛑 Watcher realtime_fdb finalizado!", flush=True)


async def main_fdb(dsn: str, user: str, password: str, manager: ConnectionManager):
    global stop_event
    stop_event.clear()
    task = asyncio.create_task(start_fdb(dsn, user, password, manager))
    try:
        await stop_event.wait()
        task.cancel()
        await task
    except asyncio.CancelledError:
        task.cancel()
        await task
    finally:
        print("✅ FDB Watcher finalizado")
