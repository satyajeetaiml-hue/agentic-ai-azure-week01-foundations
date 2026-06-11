"""Week 1 — Foundations: the IT Helpdesk Triage Agent.

Demonstrates the agent loop (reason → plan → act → observe) with one tool
(a mock KB lookup) and an escalation guardrail. Ships two backends:

* ``MockTriageBackend`` — deterministic heuristic, runs offline (default, tested).
* ``FoundryTriageBackend`` — uses Microsoft Foundry (azure-ai-projects v2,
  Responses API) to reason about the ticket, lazy-imported so Azure is optional.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── settings ────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    foundry_project_endpoint: str = ""
    foundry_model_name: str = "gpt-4o"

    @property
    def use_foundry(self) -> bool:
        return bool(self.foundry_project_endpoint)


@lru_cache
def get_settings() -> Settings:
    return Settings()


# ── schemas ─────────────────────────────────────────────────────────────
class TriageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Incoming support ticket / user message.")


class AgentStep(BaseModel):
    phase: str
    detail: str


class TriageResponse(BaseModel):
    answer: str
    category: str
    severity: str
    escalated: bool
    mode: str
    steps: list[AgentStep]


# ── shared knowledge / rules ────────────────────────────────────────────
KB: dict[str, str] = {
    "vpn": "Reset your VPN client, then reconnect with your corporate credentials.",
    "password": "Use the self-service portal to reset your password; locked accounts auto-unlock in 30 min.",
    "email": "Restart Outlook and re-add the account; check service health if many users are affected.",
}
ESCALATE_SIGNALS = ("urgent", "down", "outage", "breach", "production", "asap")

SYSTEM_INSTRUCTIONS = (
    "You are an IT helpdesk triage agent. Classify the ticket and decide how to handle it. "
    "Return ONLY JSON with keys: category (one of vpn, password, email, general), "
    "severity (normal|high), escalated (boolean), answer (string). "
    "Escalate (escalated=true) when the issue sounds urgent or affects production/many users."
)


def _kb_lookup(text: str) -> tuple[str, str | None]:
    low = text.lower()
    for key, val in KB.items():
        if key in low:
            return key, val
    return "general", None


# ── mock backend ────────────────────────────────────────────────────────
class MockTriageBackend:
    mode = "mock"

    def triage(self, message: str) -> TriageResponse:
        steps: list[AgentStep] = []
        severity = "high" if any(s in message.lower() for s in ESCALATE_SIGNALS) else "normal"
        steps.append(AgentStep(phase="reason", detail=f"Severity assessed as '{severity}'."))

        plan = "escalate" if severity == "high" else "answer_from_kb"
        steps.append(AgentStep(phase="plan", detail=f"Strategy: {plan}."))

        category, answer = _kb_lookup(message)
        steps.append(AgentStep(phase="act", detail=f"KB lookup category='{category}', hit={answer is not None}."))

        if plan == "escalate":
            final, escalated = "Escalating to a human engineer (time-sensitive).", True
        elif answer:
            final, escalated = answer, False
        else:
            final, escalated = "No KB match; routing to the helpdesk queue.", True
        steps.append(AgentStep(phase="observe", detail=f"escalated={escalated}."))

        return TriageResponse(
            answer=final, category=category, severity=severity,
            escalated=escalated, mode=self.mode, steps=steps,
        )


# ── foundry backend ─────────────────────────────────────────────────────
class FoundryTriageBackend:
    mode = "foundry"

    def triage(self, message: str) -> TriageResponse:
        steps = [AgentStep(phase="reason", detail="Asked Foundry model to classify the ticket.")]
        data = _foundry_json(SYSTEM_INSTRUCTIONS, f"Ticket: {message}")
        category = data.get("category") or "general"
        severity = data.get("severity") or "normal"
        escalated = bool(data.get("escalated"))
        # Ground the answer with the KB when available.
        _, kb_answer = _kb_lookup(message)
        answer = data.get("answer") or kb_answer or "Routing to the helpdesk queue."
        steps.append(AgentStep(phase="act", detail=f"Model returned category='{category}'."))
        steps.append(AgentStep(phase="observe", detail=f"escalated={escalated}."))
        return TriageResponse(
            answer=answer, category=category, severity=severity,
            escalated=escalated, mode=self.mode, steps=steps,
        )


def _foundry_json(system: str, user: str) -> dict[str, Any]:
    """Call the Foundry project's Responses API and parse a JSON reply."""
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    s = get_settings()
    with (
        DefaultAzureCredential() as cred,
        AIProjectClient(endpoint=s.foundry_project_endpoint, credential=cred) as proj,
    ):
        client = proj.get_openai_client()
        resp = client.responses.create(
            model=s.foundry_model_name,
            input=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        text = (resp.output_text or "{}").strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    start, end = text.find("{"), text.rfind("}")
    try:
        return json.loads(text[start : end + 1] if start != -1 else text)
    except json.JSONDecodeError:
        return {}


def get_backend():
    return FoundryTriageBackend() if get_settings().use_foundry else MockTriageBackend()
