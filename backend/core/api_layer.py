import os
from typing import List
from .paths import project_root
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def create_api_layer(project: str, events: List[AgentEvent]) -> None:
    backend_dir = os.path.join(project_root(project), "backend")
    ensure_dir(backend_dir)
    write_file(
        os.path.join(backend_dir, "api_spec.md"),
        f"""# API Spec for {project}

- GET /api/health
- POST /api/login
- POST /api/register
- GET /api/me
- POST /api/ai/music
- POST /api/ai/video
- POST /api/ai/image-to-comic
""",
    )
    # If backend/server.js already exists, we assume scaffold created it.
    # You can extend it later to wire these routes.
    events.append(AgentEvent(kind="agent", message="API backend spec extended (auth + AI endpoints)."))
