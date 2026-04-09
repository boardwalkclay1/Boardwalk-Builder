import os, subprocess
from typing import Optional
from .paths import project_root

def run_backend_dev(project: str) -> subprocess.Popen:
    root = project_root(project)
    backend_dir = os.path.join(root, "backend")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

def run_frontend_dev(project: str) -> subprocess.Popen:
    root = project_root(project)
    frontend_dir = os.path.join(root, "frontend")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
