from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.agent_routes import router as agent_router
from routes.file_routes import router as file_router
from routes.cloudflare_routes import router as cf_router
from routes.github_routes import router as gh_router
from routes.run_routes import router as run_router

app = FastAPI(title="Boardwalk AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api/agent", tags=["agent"])
app.include_router(file_router, prefix="/api/files", tags=["files"])
app.include_router(cf_router, prefix="/api/cloudflare", tags=["cloudflare"])
app.include_router(gh_router, prefix="/api/github", tags=["github"])
app.include_router(run_router, prefix="/api/run", tags=["run"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
