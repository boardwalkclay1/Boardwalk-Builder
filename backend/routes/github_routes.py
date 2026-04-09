from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from core.github_layer import clone_github_repo
from core.agent import AgentEvent

router = APIRouter()

class GitHubCloneRequest(BaseModel):
    project: str
    repo_url: str

class GitHubCloneResponse(BaseModel):
    events: List[AgentEvent]

@router.post("/clone", response_model=GitHubCloneResponse)
def api_clone_repo(req: GitHubCloneRequest):
    events: List[AgentEvent] = []
    clone_github_repo(req.project, req.repo_url, events)
    return GitHubCloneResponse(events=events)
