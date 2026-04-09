import os, subprocess
from typing import List, Optional
from .paths import project_root
from .agent import AgentEvent

def create_deploy_layer(project: str, events: List[AgentEvent]) -> None:
    root = project_root(project)
    dockerfile = os.path.join(root, "Dockerfile")
    if not os.path.exists(dockerfile):
        with open(dockerfile, "w", encoding="utf-8") as f:
            f.write("""# Example Dockerfile; adjust to your stack
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install || true
CMD ["npm", "run", "dev"]
""")
    deploy_md = os.path.join(root, "deploy.md")
    if not os.path.exists(deploy_md):
        with open(deploy_md, "w", encoding="utf-8") as f:
            f.write("""# Deployment Notes

- Use Dockerfile for container-based deployment.
- Use cloudflare/wrangler.toml for Worker deployment.
- Configure environment variables for secrets.
""")
    events.append(AgentEvent(kind="agent", message="Deployment notes and Dockerfile ensured."))

def run_cloudflare_worker_deploy(project: str, events: List[AgentEvent]) -> Optional[str]:
    cf_dir = os.path.join(project_root(project), "cloudflare")
    if not os.path.exists(cf_dir):
        events.append(AgentEvent(kind="error", message="No cloudflare directory found for project."))
        return None
    try:
        proc = subprocess.run(
            ["wrangler", "deploy"],
            cwd=cf_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        events.append(AgentEvent(kind="agent", message=f"wrangler deploy stdout:\n{proc.stdout}"))
        if proc.stderr:
            events.append(AgentEvent(kind="agent", message=f"wrangler deploy stderr:\n{proc.stderr}"))
        # You can parse URL from stdout if needed.
        return proc.stdout
    except FileNotFoundError:
        events.append(AgentEvent(kind="error", message="wrangler not found on PATH."))
        return None
