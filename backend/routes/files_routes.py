from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from core.files_layer import (
    list_project_files,
    read_project_file,
    write_project_file,
    delete_project_file,
)
from core.utils import project_exists

router = APIRouter()

class FileItem(BaseModel):
    type: str
    path: str

class FileListResponse(BaseModel):
    items: List[FileItem]

class FileReadResponse(BaseModel):
    content: str

class FileWriteRequest(BaseModel):
    project: str
    path: str
    content: str

class FileDeleteRequest(BaseModel):
    project: str
    path: str

@router.get("/list", response_model=FileListResponse)
def api_list_files(project: str):
    if not project_exists(project):
        raise HTTPException(status_code=404, detail="Project not found")
    items = list_project_files(project)
    return FileListResponse(items=[FileItem(**i) for i in items])

@router.get("/read", response_model=FileReadResponse)
def api_read_file(project: str, path: str):
    if not project_exists(project):
        raise HTTPException(status_code=404, detail="Project not found")
    content = read_project_file(project, path)
    return FileReadResponse(content=content)

@router.post("/write")
def api_write_file(req: FileWriteRequest):
    if not project_exists(req.project):
        raise HTTPException(status_code=404, detail="Project not found")
    write_project_file(req.project, req.path, req.content)
    return {"ok": True}

@router.post("/delete")
def api_delete_file(req: FileDeleteRequest):
    if not project_exists(req.project):
        raise HTTPException(status_code=404, detail="Project not found")
    delete_project_file(req.project, req.path)
    return {"ok": True}
