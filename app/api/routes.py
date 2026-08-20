from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from pydantic import BaseModel
from typing import Optional
import uuid

from app.services.job_manager import JOBS_DB, run_assessment_pipeline

router = APIRouter()

class AnalyzeRequest(BaseModel):
    github_username: str
    job_description: Optional[str] = None

@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def start_analysis(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
    # Initialize the record in our tracker
    JOBS_DB[task_id] = {
        "status": "QUEUED",
        "username": request.github_username,
        "report": None,
        "error": None
    }

    # Dispatch background task without blocking the HTTP response
    background_tasks.add_task(
        run_assessment_pipeline, 
        task_id, 
        request.github_username, 
        request.job_description
    )

    return {
        "task_id": task_id,
        "status": "QUEUED",
        "message": "Candidate analysis started in the background."
    }

@router.get("/status/{task_id}")
async def get_analysis_status(task_id: str):
    job = JOBS_DB.get(task_id)
    if not job:
        raise HTTPException(status_code=404, detail="Task ID not found")
    
    return {
        "task_id": task_id,
        "status": job["status"],
        "error": job.get("error")
    }

@router.get("/report/{task_id}")
async def get_analysis_report(task_id: str):
    job = JOBS_DB.get(task_id)
    if not job:
        raise HTTPException(status_code=404, detail="Task ID not found")
    
    if job["status"] != "COMPLETED":
        raise HTTPException(
            status_code=400, 
            detail=f"Report is not ready yet. Current status: {job['status']}"
        )
    
    return job["report"]
