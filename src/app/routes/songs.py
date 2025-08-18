import os
from fastapi import APIRouter, HTTPException, Query
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
def get_song(file: str = Query(..., description="Nome do arquivo .mp3")):
    path = os.path.join(songs_dir, file)

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    def iterfile():
        with open(path, mode="rb") as f:
            yield from f

    return StreamingResponse(
        iterfile(),
        media_type="audio/mpeg",
        headers={"Access-Control-Allow-Origin": "*"}
    )


@router.get("/songs/list")
def list_songs():
    files = []
    for root, _, filenames in os.walk(songs_dir):
        for f in filenames:
            if f.endswith(".mp3"):
                rel_path = os.path.relpath(os.path.join(root, f), songs_dir)
                files.append(rel_path)
    return {"songs": files}
