import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.utils.songs import folder_files, songs_path

router = APIRouter()
# print(f"songs: {songs_root, songs_path}")


@router.get("/music")
def get_music(file: str):
    path = os.path.join(songs_path, file)

    if not os.path.isfile(path):
        return {"error": "Arquivo não encontrado"}

    return FileResponse(path, media_type="audio/mpeg", filename=file)


@router.get("/list")
def list_songs():
    list = folder_files(songs_path)
    # print(f"list: {list}")
    return list
