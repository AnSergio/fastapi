import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.app.core.config import song_list
from src.utils.songs import folder_files

router = APIRouter()
# print(f"song_list: {song_list}")


@router.get("/music")
def get_music(file: str):
    path = os.path.join(song_list, file)

    if not os.path.isfile(path):
        return {"error": "Arquivo não encontrado"}

    return FileResponse(path, media_type="audio/mpeg", filename=file)


@router.get("/list")
def list_songs():
    list = folder_files(song_list)
    # print(f"list: {list}")
    return list
