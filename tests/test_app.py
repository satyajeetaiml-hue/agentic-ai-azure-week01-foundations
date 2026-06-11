"""Hermetic tests for the Week 1 triage agent (mock backend)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_mock():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["backend"] == "mock"


def test_answers_from_kb():
    r = client.post("/api/v1/triage", json={"message": "I forgot my password"})
    assert r.status_code == 200
    body = r.json()
    assert body["category"] == "password"
    assert body["escalated"] is False
    assert len(body["steps"]) >= 4


def test_escalates_on_urgency():
    r = client.post("/api/v1/triage", json={"message": "Production is down, urgent!"})
    assert r.status_code == 200
    body = r.json()
    assert body["severity"] == "high"
    assert body["escalated"] is True


def test_unknown_routes_to_queue():
    r = client.post("/api/v1/triage", json={"message": "My chair is broken"})
    assert r.status_code == 200
    assert r.json()["category"] == "general"


def test_validation_rejects_empty():
    r = client.post("/api/v1/triage", json={"message": ""})
    assert r.status_code == 422
