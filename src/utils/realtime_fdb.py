# src/utils/realtime_fdb.py
import os
import fdb
import psutil
import asyncio
from src.app.core.websocket import ConnectionManager

stop_event = asyncio.Event()
connect = None


def stop_fdb():
    stop_event.set()


async def start_watcher(dsn: str, user: str, password: str, manager: ConnectionManager):
    global connect
    time_delay = 1
    valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
    event_nomes = ["usuarios", "pedidos", "vendas"]

    while not stop_event.is_set():
        print(f"📡 Iniciando realtime_fdb! (delay: {time_delay}s)", flush=True)

        try:
            connect = fdb.connect(dsn=dsn, user=user, password=password)
            tasks_event = []
            time_delay = 1

            async def while_event():
                tasks_event = None
                try:
                    while not stop_event.is_set():
                        eventos = connect.event_conduit(event_nomes)
                        eventos.begin()
                        tasks_event = await asyncio.to_thread(eventos.wait, 1)
                        eventos.close()

                        for nome, event in tasks_event.items():
                            if event > 0:
                                realtime = f"firebird/{nome}"
                                # print(realtime, flush=True)
                                await manager.broadcast({"event": "realtime", "message": realtime})

                except:
                    eventos.close()
                    pass

            tasks_event.append(asyncio.create_task(while_event()))

            await asyncio.gather(*tasks_event)

        except asyncio.CancelledError:
            break

        except fdb.Error as e:
            print(f"❌ FDB Erro geral: {e}", flush=True)
            time_delay = valid_time.get(time_delay, 60)
            print(f"🔄 Reiniciando Firebird em {time_delay}s...\n", flush=True)
            await asyncio.sleep(time_delay)

        finally:
            if connect and not connect.closed:
                connect.close()

    stop_event.clear()
    # print("🛑 Watcher realtime_fdb finalizado!", flush=True)


async def main_fdb(dsn: str, user: str, password: str, manager: ConnectionManager):
    global stop_event
    stop_event.clear()
    task = asyncio.create_task(start_watcher(dsn, user, password, manager))

    try:
        await stop_event.wait()
        print("🛑 FDB Sinal de parada recebido")
        task.cancel()
        await task

    except asyncio.CancelledError:
        await asyncio.wait([task], timeout=1)
        psutil.Process(os.getpid()).terminate()
        print("🛑 FDB Watcher cancelado", flush=True)
