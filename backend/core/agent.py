from typing import List, Literal
from pydantic import BaseModel

from .paths import project_root
from .scaffold import scaffold_fullstack
from .db import create_db_layer
from .api_layer import create_api_layer
from .auth_layer import create_auth_layer
from .media_layer import create_media_layer
from .cloudflare_layer import create_cloudflare_layer
from .deploy_layer import create_deploy_layer
from .ai_apps_layer import extend_with_ai_capabilities
from .errors_layer import analyze_and_fix_errors

class AgentScope(BaseModel):
    project: str
    goal: str
    stack: str
    allow_scaffold: bool
    allow_db: bool
    allow_api: bool
    allow_auth: bool
    allow_media: bool
    allow_cloudflare: bool
    allow_frontend: bool
    allow_service_worker: bool
    allow_deploy: bool
    allow_fix: bool
    allow_ai_apps: bool = True
    mode: Literal["full", "limited"]

class AgentEvent(BaseModel):
    kind: str
    message: str

class AgentRunResult(BaseModel):
    events: List[AgentEvent]
    summary: str

def run_agent(scope: AgentScope) -> AgentRunResult:
    events: List[AgentEvent] = []
    events.append(AgentEvent(kind="system", message=f"Agent started in {scope.mode} mode for project '{scope.project}'."))

    if scope.allow_scaffold:
        scaffold_fullstack(scope.stack, scope.project, events)

    if scope.allow_db:
        create_db_layer(scope.project, events)

    if scope.allow_api:
        create_api_layer(scope.project, events)

    if scope.allow_auth:
        create_auth_layer(scope.project, events)

    if scope.allow_media:
        create_media_layer(scope.project, events)

    if scope.allow_cloudflare:
        create_cloudflare_layer(scope.project, events)

    if scope.allow_frontend or scope.allow_service_worker:
        # handled inside scaffold_fullstack or cloudflare_layer as needed
        pass

    if scope.allow_deploy:
        create_deploy_layer(scope.project, events)

    if scope.allow_ai_apps:
        extend_with_ai_capabilities(scope.project, scope.goal, events)

    summary = f"Agent completed for project '{scope.project}' with stack '{scope.stack}'."
    events.append(AgentEvent(kind="system", message=summary))
    return AgentRunResult(events=events, summary=summary)

def run_error_fix(project: str, errors: str) -> AgentRunResult:
    events: List[AgentEvent] = []
    events.append(AgentEvent(kind="system", message=f"Received error log for project '{project}'."))
    analyze_and_fix_errors(project, errors, events)
    summary = f"Diagnostics written for project '{project}'."
    events.append(AgentEvent(kind="system", message=summary))
    return AgentRunResult(events=events, summary=summary)
