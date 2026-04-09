import os
from typing import List
from .paths import project_root, safe_name
from .utils import ensure_dir, write_file
from .agent import AgentEvent

def create_media_layer(project: str, events: List[AgentEvent]) -> None:
    cf_dir = os.path.join(project_root(project), "cloudflare")
    ensure_dir(cf_dir)
    bucket_name = f"{safe_name(project)}-media"
    write_file(
        os.path.join(cf_dir, "r2.toml"),
        f"""[[r2_buckets]]
binding = "{bucket_name}"
bucket_name = "{bucket_name}"
preview_bucket_name = "{bucket_name}-preview"
""",
    )
    backend_dir = os.path.join(project_root(project), "backend")
    ensure_dir(backend_dir)
    write_file(
        os.path.join(backend_dir, "media.md"),
        f"""# Media Pipeline

- R2 bucket: {bucket_name}
- Use signed URLs for uploads/downloads.
- Wire this into your Worker or backend API.
""",
    )
    events.append(AgentEvent(kind="agent", message="Cloudflare R2 config and media notes created."))
