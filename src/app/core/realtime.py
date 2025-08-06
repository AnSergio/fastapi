import sys
import asyncio


async def on_realtime_fdb():
    python_exec = "python3" if sys.platform == "linux" else "python"
    process = await asyncio.create_subprocess_exec(
        python_exec, "realtime_fdb.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        message = line.decode().strip()
        if message.startswith("realtime/firebird/"):
            print(f"📡 Broadcast: {message}")
            # Aqui você chama seu WebSocket manager para emitir a mensagem
            # await manager.broadcast("realtime", message.replace("realtime/", ""))

    # Captura erros do stderr
    err = await process.stderr.read()
    if err:
        print(f"Python erro: {err.decode()}")

    await process.wait()
    print(f"Python finalizado Código: {process.returncode}")


async def on_realtime_mdb():
    python_exec = "python3" if sys.platform == "linux" else "python"
    process = await asyncio.create_subprocess_exec(
        python_exec, "realtime_mdb.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        message = line.decode().strip()
        if message.startswith("realtime/firebird/"):
            print(f"📡 Broadcast: {message}")
            # Aqui você chama seu WebSocket manager para emitir a mensagem
            # await manager.broadcast("realtime", message.replace("realtime/", ""))

    # Captura erros do stderr
    err = await process.stderr.read()
    if err:
        print(f"Python erro: {err.decode()}")

    await process.wait()
    print(f"Python finalizado Código: {process.returncode}")
