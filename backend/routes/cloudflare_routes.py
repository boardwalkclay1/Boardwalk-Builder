from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from core.deploy_layer import run_cloudflare_worker_deploy
from core.agent import AgentEvent

router = APIRouter()

class CFDeployRequest(BaseModel):
    project: str

class CFDeployResponse(BaseModel):
    events: List[AgentEvent]
    output: Optional[str] = None

@router.post("/deploy_worker", response_model=CFDeployResponse)
def api_deploy_worker(req: CFDeployRequest):
    events: List[AgentEvent] = []
    output = run_cloudflare_worker_deploy(req.project, events)
    return CFDeployResponse(events=events, output=output)
