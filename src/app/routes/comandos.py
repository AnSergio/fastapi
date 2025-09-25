# src/app/routes/comandos.py
import platform
import subprocess
from fastapi import APIRouter, HTTPException
from src.app.schemas.comando import ComandoLinuxRequest, ComandoWindowsRequest

router = APIRouter()


@router.post("/linux")
async def on_comando_linux(body: ComandoLinuxRequest):
    # print(f"body: {body}")
    nome = body.nome.strip()
    comando = body.comando.strip().lower()

    if not nome or not comando:
        raise HTTPException(status_code=400, detail="Nome e comando são necessários!")

    if platform.system().lower() != "linux":
        raise HTTPException(status_code=400, detail="Sistema Linux é necessário!")

    valid_commands = {
        "start":   ["sudo", "systemctl", "start", nome],
        "stop":    ["sudo", "systemctl", "stop", nome],
        "restart": ["sudo", "systemctl", "restart", nome],
        "status":  ["systemctl", "is-active", nome],
    }

    action = valid_commands.get(comando)
    if not action:
        raise HTTPException(status_code=400, detail="Comando inválido!")

    try:
        result = subprocess.run(
            action,
            text=True,
            capture_output=True
        )

        output = result.stdout.strip()
        stderr = result.stderr.strip()

        # Se for status, tratamos diferente
        if comando == "status":
            return {"status": output == "active", "comando": comando}

        # Para start/stop/restart, verificamos se houve erro
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr or "Erro desconhecido")

        return {"status": True, "comando": comando}

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())


@router.post("/win")
async def on_comando_win(body: ComandoWindowsRequest):
    print(f"body: {body}")
    comando = body.comando

    if not comando:
        raise HTTPException(status_code=400, detail="Comando são necessários!")

    if platform.system().lower() != "windows":
        raise HTTPException(status_code=400, detail=f"Sistema Windows é necessário!")

    if not comando:
        raise HTTPException(status_code=400, detail="Comando inválido!")

    try:
        result = subprocess.run(comando, shell=True, text=True, capture_output=True)
        output = result.stdout.strip()

        if result.returncode != 0 and output != "inactive":
            raise HTTPException(status_code=500, detail=result.stderr.strip())

        # print(f"Comando executado: {action}, Saída: {output}")
        status = True if output else False
        return {"status": status, "retorno": output}

    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())
