import os
from typing import List
from .paths import project_root

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_file(path: str, content: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_dir_recursive(root: str) -> List[dict]:
    items = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        for d in dirnames:
            items.append({
                "type": "dir",
                "path": os.path.join(rel, d).replace("\\", "/")
            })
        for f in filenames:
            items.append({
                "type": "file",
                "path": os.path.join(rel, f).replace("\\", "/")
            })
    return items

def project_exists(project: str) -> bool:
    return os.path.exists(project_root(project))
