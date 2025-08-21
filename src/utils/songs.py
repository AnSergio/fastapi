import os

songs_root = os.path.join(os.path.dirname(os.path.dirname(__file__)))
# print(f"songs_root: {songs_root}")
songs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "songs")
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
