import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.dirname(BASE_DIR)
FILES_DIR = os.path.join(BACKEND_ROOT, "boardwalk_files")

os.makedirs(FILES_DIR, exist_ok=True)

def safe_name(name: str) -> str:
    return name.replace("..", "_").strip().replace(" ", "-")

def project_root(project: str) -> str:
    from .paths import FILES_DIR  # avoid circular
    return os.path.join(FILES_DIR, safe_name(project))
