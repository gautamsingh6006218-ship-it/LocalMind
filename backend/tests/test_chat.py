from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_endpoint_returns_200():
    response = client.post("/chat", json={"question": "What is the meaning of life?"})

    assert response.status_code == 200


def test_chat_endpoint_response_shape():
    response = client.post("/chat", json={"question": "What is the meaning of life?"})
    body = response.json()

    assert "answer" in body
    assert isinstance(body["answer"], str)
    assert len(body["answer"]) > 0


def test_chat_endpoint_rejects_missing_question():
    # No "question" field in the body - FastAPI/Pydantic should reject this
    # automatically (422 Unprocessable Entity) before our code even runs.
    response = client.post("/chat", json={})

    assert response.status_code == 422
