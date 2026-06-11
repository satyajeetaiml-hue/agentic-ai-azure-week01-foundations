"""Week 1 — Foundations of Agentic AI.

IT Helpdesk Triage Agent. Runs in MOCK mode out of the box; set
FOUNDRY_PROJECT_ENDPOINT (+ `az login`) for the Foundry backend.
Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.service import TriageRequest, TriageResponse, get_backend, get_settings

settings = get_settings()
app = FastAPI(title="Week 1 — Foundations (Triage Agent)", version="0.2.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "week": "1",
        "backend": "foundry" if settings.use_foundry else "mock",
    }


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": "agentic-ai-azure-week01-foundations",
        "endpoint": "/api/v1/triage",
        "backend": "foundry" if settings.use_foundry else "mock",
        "docs": "/docs",
    }


@app.post("/api/v1/triage", response_model=TriageResponse, tags=["week01"])
def triage(payload: TriageRequest) -> TriageResponse:
    return get_backend().triage(payload.message)
