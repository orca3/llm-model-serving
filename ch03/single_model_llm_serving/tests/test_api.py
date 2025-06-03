import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate():
    response = client.post(
        "/generate",
        json={"prompt": "Hello, I am"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "generated_text" in data
    assert isinstance(data["generated_text"], str)
    assert len(data["generated_text"]) > 0 