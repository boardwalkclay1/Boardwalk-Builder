import os
from typing import List, Optional
from .paths import project_root
from .utils import list_dir_recursive, read_file, write_file
from .agent import AgentEvent

def list_project_files(project: str) -> List[dict]:
    root = project_root(project)
    return list_dir_recursive(root)

def read_project_file(project: str, rel_path: str) -> str:
    root = project_root(project)
    full = os.path.join(root, rel_path)
    return read_file(full)

def write_project_file(project: str, rel_path: str, content: str) -> None:
    root = project_root(project)
    full = os.path.join(root, rel_path)
    write_file(full, content)

def delete_project_file(project: str, rel_path: str) -> None:
    root = project_root(project)
    full = os.path.join(root, rel_path)
    if os.path.exists(full):
        os.remove(full)
