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

def test_generate_batch():
    # Test with multiple prompts
    test_prompts = [
        "Hello, I am",
        "The weather is",
        "I want to",
        "The best way to"
    ]
    
    response = client.post(
        "/generate_batch",
        json={"prompts": test_prompts}
    )
    
    # Check response status and structure
    assert response.status_code == 200
    data = response.json()
    assert "generated_texts" in data
    assert isinstance(data["generated_texts"], list)
    
    # Verify we got results for all prompts
    assert len(data["generated_texts"]) == len(test_prompts)
    
    # Verify each generated text is valid
    for generated_text in data["generated_texts"]:
        assert isinstance(generated_text, str)
        assert len(generated_text) > 0 