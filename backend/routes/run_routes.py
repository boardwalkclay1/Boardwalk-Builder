from fastapi import APIRouter
from pydantic import BaseModel

from core.runners_layer import run_backend_dev, run_frontend_dev

router = APIRouter()

# NOTE: This is a simple fire-and-forget runner.
# For full control (stop, logs), you’d track Popen objects in memory.

class RunRequest(BaseModel):
    project: str

@router.post("/backend")
def api_run_backend(req: RunRequest):
    run_backend_dev(req.project)
    return {"ok": True, "message": "Backend dev server started (npm run dev)."}

@router.post("/frontend")
def api_run_frontend(req: RunRequest):
    run_frontend_dev(req.project)
    return {"ok": True, "message": "Frontend dev server started (npm run dev)."}
