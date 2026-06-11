"""Smoke tests for Week 1 — Foundations of Agentic AI."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_endpoint_accepts_input():
    r = client.post("/api/v1/triage", json={"message": "My laptop won't connect to VPN and it's urgent"})
    assert r.status_code == 200


def test_endpoint_rejects_empty():
    r = client.post("/api/v1/triage", json={"message": ""})
    assert r.status_code == 422
