# GitHub Candidate Assessment Engine - Backend

An automated evaluation pipeline that ingests GitHub metadata, performs shallow repository cloning for static AST analysis, and generates candidate scoring reports.

## Tech Stack
- **Framework:** FastAPI (Python 3.10+)
- **Data Ingestion:** GitHub GraphQL API
- **Task Orchestration:** Asynchronous Background Tasks
- **HTTP Client:** HTTPX (Async)

## Project Structure
```text
├── app/
│   ├── api/          # Route handlers & endpoints
│   ├── services/     # GitHub GraphQL & Repo cloning services
│   └── main.py       # FastAPI application entry point
├── .env.example      # Sample environment configuration
├── .gitignore
├── requirements.txt
└── README.md
