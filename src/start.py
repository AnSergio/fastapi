# src/dev.py
import sys
import signal
import subprocess
from src.app.core.config import host, port


def main():
    print("🚀 Iniciando FastAPI\n")

    # Inicia uvicorn em subprocesso
    process = subprocess.Popen(["uv", "run", "uvicorn", "src.app.main:app", "--host", host, "--port", str(port)])

    try:
        # Aguarda o processo terminar normalmente
        process.wait()
    except KeyboardInterrupt:
        try:
            process.send_signal(signal.SIGINT)  # envia Ctrl+C para o subprocesso
            process.wait(timeout=5)
            print("\n⛔ Recebido Ctrl+C! Encerrando FastAPI...")
        except subprocess.TimeoutExpired:
            print("⚠️ Timeout: Forçando encerramento.")
            process.kill()
        sys.exit(0)


if __name__ == "__main__":
    main()
