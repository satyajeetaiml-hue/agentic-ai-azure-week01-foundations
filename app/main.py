"""Week 1 — Foundations of Agentic AI — runnable IT Helpdesk Triage Agent.

Demonstrates the core agent loop: reason → plan → act → observe, with one tool
(a mock KB lookup) and an escalation guardrail. Runs with zero Azure dependencies.
Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Week 1 — Foundations of Agentic AI", version="0.1.0")

# Mock "knowledge base" standing in for Azure AI Search (Week 8).
_KB = {
    "vpn": "Reset your VPN client, then reconnect with your corporate credentials.",
    "password": "Use the self-service portal to reset your password; locked accounts auto-unlock in 30 min.",
    "email": "Restart Outlook and re-add the account; check service health if many users are affected.",
}
_ESCALATE = ("urgent", "down", "outage", "breach", "production", "asap")


class LabRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Incoming support ticket / user message.")


def _lookup(text):
    low = text.lower()
    for key, val in _KB.items():
        if key in low:
            return key, val
    return "general", None


@app.get("/health")
def health():
    return {"status": "ok", "week": "1", "use_case": "IT Helpdesk Triage Agent"}


@app.get("/")
def root():
    return {"service": "agentic-ai-azure-week01-foundations", "week": "1", "endpoint": "/api/v1/triage", "docs": "/docs"}


@app.post("/api/v1/triage")
def triage(payload: LabRequest):
    steps = []
    text = payload.message

    # REASON
    severity = "high" if any(s in text.lower() for s in _ESCALATE) else "normal"
    steps.append({"phase": "reason", "detail": f"Severity assessed as '{severity}'."})

    # PLAN
    plan = "escalate" if severity == "high" else "answer_from_kb"
    steps.append({"phase": "plan", "detail": f"Strategy: {plan}."})

    # ACT
    category, answer = _lookup(text)
    steps.append({"phase": "act", "detail": f"KB lookup category='{category}', hit={answer is not None}."})

    # OBSERVE
    if plan == "escalate":
        final, escalated = "Escalating to a human engineer (time-sensitive).", True
    elif answer:
        final, escalated = answer, False
    else:
        final, escalated = "No KB match; routing to the helpdesk queue.", True
    steps.append({"phase": "observe", "detail": f"escalated={escalated}."})

    return {
        "answer": final,
        "category": category,
        "escalated": escalated,
        "severity": severity,
        "steps": steps,
    }
