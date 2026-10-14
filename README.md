# GitHub Candidate Assessment Engine (Backend)

Backend for the **AI - Candidate Assessment Platform**, an automated pipeline that evaluates a candidate's GitHub presence. It collects profile and repository metadata, shallow-clones repositories for static AST analysis, and produces candidate scoring reports.

> Final Year Project

## Features

- Ingests GitHub profile and repository metadata through the GitHub GraphQL API
- Shallow-clones candidate repositories for analysis
- Static code analysis using AST parsing
- Generates candidate scoring reports
- Runs long evaluations as background tasks so API requests don't block

## Tech Stack

- **Framework:** FastAPI (Python 3.10+)
- **Data source:** GitHub GraphQL API
- **HTTP client:** HTTPX (async)
- **Orchestration:** Asynchronous background tasks

## Project Structure

```
.
├── app/
│   ├── api/            # Route handlers and endpoints
│   ├── services/       # GitHub GraphQL and repository-cloning services
│   └── main.py         # FastAPI entry point
├── frontend/           # Frontend client
├── tests/              # Test suite
├── test_repo/          # Sample repository used for testing
├── test_github.py      # GitHub integration test script
├── .env.example        # Example environment configuration
├── requirements.txt    # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A GitHub personal access token (needed for the GraphQL API)

### Installation

```bash
git clone https://github.com/ayaanmanara/AI---Candidate-Assessment-Platform.git
cd AI---Candidate-Assessment-Platform

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

<!-- TODO: list the variables from .env.example (e.g. the GitHub token variable name) -->

### Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Testing

```bash
pytest tests/
```

<!-- TODO: confirm the test command and describe test_github.py -->

## Frontend

<!-- TODO: add setup/run steps for the frontend/ directory -->

## API Overview

<!-- TODO: document the main endpoints under app/api/ -->

## License

<!-- TODO: add a license -->
