import pytest
from fastapi.testclient import TestClient
from main import app
import httpx

client = TestClient(app)

def test_generate_vllm_single_prompt():
    """Test vLLM generation with a single prompt"""
    response = client.post(
        "/generate_vllm",
        json={"prompts": ["Hello, I am"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "generated_texts" in data
    assert len(data["generated_texts"]) == 1
    assert isinstance(data["generated_texts"][0], str)
    assert len(data["generated_texts"][0]) > 0

def test_generate_vllm_multiple_prompts():
    """Test vLLM generation with multiple prompts"""
    prompts = [
        "Hello, I am",
        "The weather is",
        "Once upon a time"
    ]
    response = client.post(
        "/generate_vllm",
        json={"prompts": prompts}
    )
    assert response.status_code == 200
    data = response.json()
    assert "generated_texts" in data
    assert len(data["generated_texts"]) == len(prompts)
    for text in data["generated_texts"]:
        assert isinstance(text, str)
        assert len(text) > 0

def test_generate_vllm_empty_prompts():
    """Test vLLM generation with empty prompts list"""
    response = client.post(
        "/generate_vllm",
        json={"prompts": []}
    )
    assert response.status_code == 200
    data = response.json()
    assert "generated_texts" in data
    assert len(data["generated_texts"]) == 0

def test_generate_vllm_invalid_request():
    """Test vLLM generation with invalid request format"""
    response = client.post(
        "/generate_vllm",
        json={"invalid_field": ["Hello"]}
    )
    assert response.status_code == 422  # Validation error 