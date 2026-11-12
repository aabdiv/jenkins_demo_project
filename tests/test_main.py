from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 201
    assert response.json() == {"status": "ok"}


def test_ask_echoes_question() -> None:
    response = client.post("/ask", json={"text": "  что такое Jenkins?  "})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Вы спросили: что такое Jenkins?"
    assert body["length"] == len("что такое Jenkins?")


def test_ask_requires_text() -> None:
    response = client.post("/ask", json={})
    assert response.status_code == 422
