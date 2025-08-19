import os
from fastapi import APIRouter, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, StreamingResponse
from src.utils.songs import songs_dir

router = APIRouter()


@router.get("/songs2")
def get_song2(file: str = Query(..., description="Nome do arquivo .mp3")):
    path = os.path.join(songs_dir, file)

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    headers = {"Access-Control-Allow-Origin": "*"}
    return FileResponse(
        path,
        media_type="audio/mpeg",
        filename=file,
        headers=headers
    )


@router.get("/songs")
def get_song(file: str, request: Request):
    path = os.path.join(songs_dir, file)

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    file_size = os.path.getsize(path)
    range_header = request.headers.get("Range")
    if range_header:
        # Exemplo: "bytes=1000-"
        range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if range_match:
            start = int(range_match.group(1))
            end = range_match.group(2)
            end = int(end) if end else file_size - 1
            length = end - start + 1

            with open(path, "rb") as f:
                f.seek(start)
                data = f.read(length)

            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(length),
                "Content-Type": "audio/mpeg",
            }
            return Response(content=data, status_code=206, headers=headers)

    # fallback: envia tudo
    return FileResponse(path, media_type="audio/mpeg", headers={"Accept-Ranges": "bytes"})


@router.get("/songs/list")
def list_songs():
    files = []
    for root, _, filenames in os.walk(songs_dir):
        for f in filenames:
            if f.endswith(".mp3"):
                rel_path = os.path.relpath(os.path.join(root, f), songs_dir)
                files.append(rel_path)
    return {"songs": files}
