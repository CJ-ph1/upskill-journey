"""End-to-end flow test: API → Service → Repository → DB.

Run with:
    pip install -e ".[dev]"
    pytest
"""
from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_create_and_list_student():
    payload = {"name": "Grace Hopper", "email": "grace@example.com", "age": 41}
    r = client.post("/students", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "grace@example.com"
    assert "id" in body

    r = client.get("/students")
    assert r.status_code == 200
    emails = [s["email"] for s in r.json()]
    assert "grace@example.com" in emails


def test_invalid_email_is_rejected_by_service():
    r = client.post(
        "/students",
        json={"name": "Bad", "email": "no-at-sign", "age": 20},
    )
    assert r.status_code == 400
    assert "email" in r.json()["detail"]


def test_negative_age_is_rejected_by_service():
    r = client.post(
        "/students",
        json={"name": "Time Traveller", "email": "tt@example.com", "age": -1},
    )
    assert r.status_code == 400
    assert "age" in r.json()["detail"]
