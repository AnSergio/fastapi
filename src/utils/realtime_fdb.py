# src/utils/realtime_fdb.py
import time
import threading
import fdb

# Eventos Firebird que serão monitorados
event_nomes = ["cp_pedido", "cp_pedido_item", "tnfcanfen", "tnfcanfsa", "tnfitnfen", "tnfitnfsa"]

# Retry progressivo (em segundos)
valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
initial_time = 1

# Controle externo
active_threads = []
stop_event = threading.Event()


def stop_fdb():
    stop_event.set()


def start_watcher(connect, time_delay):
    def on_restart():
        nonlocal time_delay
        time_delay = valid_time[time_delay]
        raise RuntimeError("Restart requested")

    try:
        time_delay = 1  # Reset tempo após sucesso

        while True:
            eventos = connect.event_conduit(event_nomes)
            eventos.begin()
            result = eventos.wait()
            eventos.close()

            for nome, event in result.items():
                if event > 0:
                    print(f"realtime/firebird/{nome}", flush=True)

    except KeyboardInterrupt:
        print("Interrompido manualmente", flush=True)
        raise
    except Exception as e:
        print(f"Erro em watch: {e}", flush=True)
        on_restart()


def main_fdb(dsn: str, user: str, password: str):
    global active_threads
    time_delay = initial_time

    while not stop_event.is_set():
        stop_event.clear()
        active_threads = []

        print(f"📡 Iniciando realtime_fdb! (delay: {time_delay}s)", flush=True)
        connect = fdb.connect(dsn=dsn, user=user, password=password)
        thread = threading.Thread(
            target=start_watcher,
            args=(connect, time_delay),
            daemon=True
        )
        thread.start()
        active_threads.append(thread)

        while thread.is_alive() and not stop_event.is_set():
            time.sleep(1)

        if stop_event.is_set():
            break

        print(f"🔄 Reiniciando Firebird em {time_delay}s...\n", flush=True)
        time.sleep(time_delay)

    print("🛑 Watcher realtime_fdb finalizado!", flush=True)
