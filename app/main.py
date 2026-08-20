from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="GitHub Candidate Assessment Engine",
    description="Backend API for automated code evaluation and profile analysis",
    version="1.0.0"
)

# Allow Team Member 1 (Next.js frontend) to call this API without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount our routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "running", "service": "GitHub Candidate Assessment Backend"}
