import os
from src.app.core.config import song_list

# songs_path = os.path.join(song_list)
# print(f"songs_path: {songs_path}")


def folder_files(path):
    tree = {"name": os.path.basename(path), "files": [], "folders": []}
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                tree["folders"].append(folder_files(entry.path))
            elif entry.is_file() and entry.name.endswith(".mp3"):
                tree["files"].append(entry.name)
    except PermissionError:
        pass
    return tree
