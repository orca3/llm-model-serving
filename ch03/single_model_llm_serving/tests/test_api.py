import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
import asyncio
import json
import threading
import time
from contextlib import asynccontextmanager

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    print("Creating event loop...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    print("Closing event loop...")
    loop.close()

@pytest.fixture(scope="session")
def test_app():
    """Create a test app."""
    print("Setting up test app...")
    return app

@pytest.fixture
def client(test_app):
    """Create a test client with the test app."""
    return TestClient(test_app)

@pytest.fixture
async def async_client(test_app, event_loop):
    """Create an async test client with the test app."""
    print("Creating async client...")
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac

def test_generate(client):
    response = client.post(
        "/basic_generate",
        json={"prompt": "Hello, I am"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "generated_text" in data
    assert isinstance(data["generated_text"], str)
    assert len(data["generated_text"]) > 0

def test_generate_batch(client):
    # Test with multiple prompts
    test_prompts = [
        "Hello, I am",
        "The weather is",
        "I want to",
        "The best way to", 
        "The most efficient way to"
    ]
    
    response = client.post(
        "/generate",
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

@pytest.mark.asyncio
async def test_generate_stream(async_client):
    print("Starting test_generate_stream...")
    
    prompt = "Hello, I am"
    # Create a streaming request with stream=True
    async with async_client.stream("POST", "/generate_stream", json={"prompt": prompt}) as response:
        assert response.status_code == 200
        
        # Collect all tokens
        tokens = []
        sequence_ids = set()
        
        # Process the response stream directly
        async for chunk in response.aiter_bytes():
            if chunk:
                # Convert bytes to string and split by newlines
                lines = chunk.decode().split('\n')
                for line in lines:
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        token = data["token"]
                        print(f"Received token: {token}")  # Debug print
                        tokens.append(token)
                        sequence_ids.add(data["sequence_id"])
        
        # Verify we got some tokens
        assert len(tokens) > 0
        # Verify we got a sequence ID
        assert len(sequence_ids) == 1
        # Verify tokens form a coherent text
        generated_text = "".join(tokens)
        assert len(generated_text) > 0
        print(f"Final generated text: {prompt} {generated_text}")

@pytest.mark.asyncio
async def test_generate_stream_concurrent(async_client):
    print("Starting test_generate_stream_concurrent...")
    
    async def make_stream_request(prompt):
        tokens = []
        async with async_client.stream("POST", "/generate_stream", json={"prompt": prompt}) as response:
            assert response.status_code == 200
            async for chunk in response.aiter_bytes():
                if chunk:
                    lines = chunk.decode().split('\n')
                    for line in lines:
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            token = data["token"]
                            print(f"Received token for prompt '{prompt}': {token}")
                            tokens.append(token)
        return tokens

    # Create two concurrent requests
    prompt1 = "Hello, I am"
    prompt2 = "I would like to"
    
    # Run both requests concurrently
    tokens1, tokens2 = await asyncio.gather(
        make_stream_request(prompt1),
        make_stream_request(prompt2)
    )
    
    # Verify results
    assert len(tokens1) > 0, "No tokens received for first prompt"
    assert len(tokens2) > 0, "No tokens received for second prompt"
    
    # Verify tokens form coherent text
    generated_text1 = "".join(tokens1)
    generated_text2 = "".join(tokens2)
    
    print(f"Generated text 1: {generated_text1}")
    print(f"Generated text 2: {generated_text2}")
    
    assert len(generated_text1) > 0, "Empty generated text for first prompt"
    assert len(generated_text2) > 0, "Empty generated text for second prompt"
    
    # Verify the generated texts are different
    assert generated_text1 != generated_text2, "Generated texts should be different for different prompts" 