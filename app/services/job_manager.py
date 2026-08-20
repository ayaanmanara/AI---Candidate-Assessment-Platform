import uuid
import asyncio
from typing import Dict, Any
from app.services.github_service import fetch_github_data
from app.services.repo_cloner import clone_repositories, cleanup_cloned_repos

# In-memory store for task states (In production, replace with Redis or Postgres)
JOBS_DB: Dict[str, Dict[str, Any]] = {}

async def run_assessment_pipeline(task_id: str, username: str, job_description: str | None):
    try:
        # Stage 1: Fetch metadata via GraphQL (Member 2)
        JOBS_DB[task_id]["status"] = "FETCHING_GITHUB_METADATA"
        raw_github = await fetch_github_data(username)
        
        # Extract non-forked repo names
        repo_nodes = raw_github.get("repositories", {}).get("nodes", [])
        repo_names = [r["name"] for r in repo_nodes if not r.get("isFork")]

        # Stage 2: Shallow clone candidate code (Member 2)
        JOBS_DB[task_id]["status"] = "CLONING_REPOSITORIES"
        cloned_paths = await asyncio.to_thread(clone_repositories, username, repo_names, max_repos=3)

        # Stage 3: Static Analysis Hook (Member 3 will attach their function here)
        JOBS_DB[task_id]["status"] = "RUNNING_STATIC_ANALYSIS"
        await asyncio.sleep(2)  # Simulating static analysis execution
        mock_static_results = {
            "authenticity_score": 88.5,
            "cyclomatic_complexity": "Low",
            "has_unit_tests": any("test" in name.lower() for name in repo_names),
            "detected_secrets": 0
        }

        # Stage 4: AI Matching Hook (Member 4 will attach their function here)
        JOBS_DB[task_id]["status"] = "RUNNING_AI_EVALUATION"
        await asyncio.sleep(2)  # Simulating LLM analysis
        mock_ai_results = {
            "jd_match_percentage": 82,
            "matched_skills": ["JavaScript", "HTML"],
            "interview_questions": [
                f"In your repository '{repo_names[0] if repo_names else 'project'}', how did you organize your frontend assets and state management?"
            ]
        }

        # Stage 5: Cleanup cloned files from disk
        cleanup_cloned_repos(cloned_paths)

        # Stage 6: Final Combined Report Assembly
        JOBS_DB[task_id]["status"] = "COMPLETED"
        JOBS_DB[task_id]["report"] = {
            "candidate": {
                "username": raw_github.get("login"),
                "avatar_url": raw_github.get("avatarUrl"),
                "total_contributions": raw_github["contributionsCollection"]["contributionCalendar"]["totalContributions"],
            },
            "authenticity_and_quality": mock_static_results,
            "jd_match_and_interview": mock_ai_results
        }

    except Exception as e:
        JOBS_DB[task_id]["status"] = "FAILED"
        JOBS_DB[task_id]["error"] = str(e)
