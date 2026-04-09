from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from core.agent import AgentScope, run_agent, run_error_fix, AgentEvent, AgentRunResult

router = APIRouter()

class AgentRunResponse(BaseModel):
    events: List[AgentEvent]
    summary: str

class FixErrorsRequest(BaseModel):
    project: str
    errors: str

class FixErrorsResponse(BaseModel):
    events: List[AgentEvent]
    summary: str

@router.post("/run", response_model=AgentRunResponse)
def api_agent_run(scope: AgentScope):
    return run_agent(scope)

@router.post("/fix_errors", response_model=FixErrorsResponse)
def api_fix_errors(req: FixErrorsRequest):
    return run_error_fix(req.project, req.errors)
