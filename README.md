# Week 1 — Foundations of Agentic AI

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/actions/workflows/ci.yml)

> ▶️ **Run in VS Code — no Azure needed.** `pip install -r requirements.txt`, then `uvicorn app.main:app --reload` and open http://127.0.0.1:8000/docs. Runs in **mock mode** by default — no `az login`, keys, or `.env` required. Wiring real Azure (below) is optional.

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class*.
> Course hub: [azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass).

---

## 🎯 Learning goal
Understand the **agent loop** (reason → plan → act → observe), tool use, and the agent contract.

## 🏢 Enterprise use case — "IT Helpdesk Triage Agent" (Cross-industry)
A single agent reads a support ticket, reasons about category/severity, and either answers from a
knowledge base (a **tool**) or escalates to a human (a **guardrail**).

## ✅ What this repo implements
- **Mock backend** — deterministic reason→plan→act→observe loop with a KB-lookup tool and escalation
  rule. Runs offline and is fully tested.
- **Foundry backend** — uses Microsoft Foundry (azure-ai-projects v2, Responses API) to classify the
  ticket, grounded by the KB. Lazy-imported, selected when `FOUNDRY_PROJECT_ENDPOINT` is set.

| Condition | Backend |
|-----------|---------|
| `FOUNDRY_PROJECT_ENDPOINT` unset | `mock` (default) |
| `FOUNDRY_PROJECT_ENDPOINT` set + `az login` | `foundry` |

## 🚀 Quick start
```bash
python -m venv .venv && .\.venv\Scripts\Activate.ps1   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "Production is down, this is urgent!"}'
```
Run tests: `pytest -q`

## ☁️ Foundry mode
`az login`, then set in `.env`:
```
FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
FOUNDRY_MODEL_NAME=gpt-4o
```
`GET /health` will report `"backend": "foundry"`.

## 🏗️ Architect's lens
- When is an *agent* right vs. a deterministic workflow or single LLM call? (cost, latency, auditability)
- Foundry vs. Agent Framework vs. raw model calls.
- The **agent contract**: inputs, tools, guardrails, success criteria.

## 🧰 Tech stack
FastAPI, Pydantic v2, Microsoft Foundry (azure-ai-projects v2, Responses API), azure-identity.

## 📁 Structure
```
app/service.py   # settings + schemas + mock & foundry backends
app/main.py      # FastAPI app + POST /api/v1/triage
tests/test_app.py
```

## 🗺️ Series
Next: [Week 2 — Foundry Claims Intake](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week02-foundry-claims).
All labs: [search `agentic-ai-azure`](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure).

## 📄 License
MIT — see [`LICENSE`](LICENSE).
