import sys
import time
import fdb

# Conexão Firebird
USER = "SYSDBA"
PASSWORD = "masterkey"

# Eventos Firebird que serão monitorados
event_nomes = ["cp_pedido", "cp_pedido_item", "tnfcanfen", "tnfcanfsa", "tnfitnfen", "tnfitnfsa"]

# Retry progressivo (em segundos)
valid_time = {1: 2, 2: 5, 5: 10, 10: 30, 30: 60, 60: 60}
initial_time = 1


def start_watch(connect, time_delay):
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


def main(DSN: str):
    time_delay = initial_time

    while True:
        try:
            print(f"\n Iniciando monitoramento... (delay atual: {time_delay}s)\n", flush=True)
            connect = fdb.connect(dsn=DSN, user=USER, password=PASSWORD)
            start_watch(connect, time_delay)
        except RuntimeError:
            print(f"Reiniciando em {time_delay}s...\n", flush=True)
            time.sleep(time_delay)
        except KeyboardInterrupt:
            print("Encerrando...", flush=True)
            break
        finally:
            try:
                connect.close()
                print("Conexão fechada\n", flush=True)
            except:
                pass


if __name__ == "__main__":
    DSN = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:/home/firebird/dados.fdb'
    main(DSN)
