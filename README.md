# Week 1 — Foundations of Agentic AI

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/actions/workflows/ci.yml)

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class* (12 weeks).
> Each lab is an independent, runnable FastAPI starter. Part of the
> [course series](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure).

---

## 🎯 Learning goal
Understand agent loops (reason → plan → act → observe), tool use, and where each Azure service fits.

## 🏢 Enterprise use case — "IT Helpdesk Triage Agent" (Cross-industry)
A single agent reads an incoming support ticket, reasons about category/severity, and either answers from a knowledge base or escalates to a human. This establishes the core mental model before adding complexity.

---

## 🧪 What you'll build (lab)
1. Build a "hello agent" with a reasoning loop + one tool (a ticket/KB lookup mock).
2. Run it locally and expose it as a FastAPI `/triage` endpoint.
3. Define your **agent contract**: inputs, tools, guardrails, and success criteria.
4. Add a guardrail that escalates urgent/high-severity tickets to a human.

> This starter ships with a **runnable mock** of the endpoint so you can run and test
> immediately, then progressively replace the mock with the real Azure implementation.

## 🏗️ Architect's lens
- When is an *agent* the right pattern vs. a deterministic workflow or a single LLM call? (Cost, latency, auditability.)
- Map the Azure agentic landscape: Foundry vs. Agent Framework vs. raw model calls.
- Treat the agent contract as a first-class artifact you version and test.

## 🧰 Tech stack
Python 3.11+, FastAPI, Pydantic, Microsoft Foundry, Azure OpenAI / Foundry models, uvicorn.

---

## 🚀 Quick start

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) copy the env template — runs in MOCK mode without it
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run the API
uvicorn app.main:app --reload
```

Open the interactive docs at **http://127.0.0.1:8000/docs**.

### Try the endpoint
```bash
curl -X POST http://127.0.0.1:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "My laptop won't connect to VPN and it's urgent"}'
```

### Run the tests
```bash
pytest -q
```

### Run with Docker
```bash
docker build -t agentic-ai-azure-week01-foundations .
docker run -p 8000:8000 agentic-ai-azure-week01-foundations
```

---

## 📁 Project structure
```
agentic-ai-azure-week01-foundations/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app + the /api/v1/triage endpoint
├── tests/
│   └── test_smoke.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 🗺️ Where this fits
This repo covers **Week 1 — Foundations of Agentic AI**. The full 12-week path and reference architecture
live in the master-class companion repo:
**[azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass)**.

## 📄 License
MIT — see [`LICENSE`](LICENSE).
