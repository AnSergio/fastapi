import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.utils.songs import songs_dir

router = APIRouter()


def build_tree(path, id_counter=[1]):
    node_id = id_counter[0]
    id_counter[0] += 1

    node = {
        "id": node_id,
        "title": os.path.basename(path),
        "children": []
    }

    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                node["children"].append(build_tree(entry.path, id_counter))
            elif entry.is_file() and entry.name.endswith(".mp3"):
                file_id = id_counter[0]
                id_counter[0] += 1
                node["children"].append({
                    "id": file_id,
                    "title": entry.name
                })
    except PermissionError:
        pass

    return node


@router.get("/music")
def get_song(file: str):
    path = os.path.join(songs_dir, file)

    if not os.path.isfile(path):
        return {"error": "Arquivo não encontrado"}

    return FileResponse(path, media_type="audio/mpeg", filename=file)


@router.get("/list")
def list_songs():
    return [build_tree(songs_dir)]
