import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.utils.songs import songs_dir

router = APIRouter()


def build_tree(path):
    tree = {"name": os.path.basename(path), "files": [], "folders": []}
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                tree["folders"].append(build_tree(entry.path))
            elif entry.is_file() and entry.name.endswith(".mp3"):
                tree["files"].append(entry.name)
    except PermissionError:
        pass
    return tree


@router.get("/music")
def get_song(file: str):
    path = os.path.join(songs_dir, file)

    if not os.path.isfile(path):
        return {"error": "Arquivo não encontrado"}

    return FileResponse(path, media_type="audio/mpeg", filename=file)


@router.get("/list")
def list_songs():
    return build_tree(songs_dir)
