# Simple LLM Serving Demo

This is a simple demonstration of how to serve a single LLM model using FastAPI. The service uses the facebook/opt-125m model and implements a basic serving architecture with workload management and model execution in a separate process. It also includes vLLM integration for efficient batched inference.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

Start the service:
```bash
python main.py
```

The service will be available at http://localhost:8000

## API Usage

### Basic Generation
Send a POST request to `/generate` with a JSON body:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompts": ["Hello, I am"]}'
```

### vLLM Generation
For efficient batched inference using vLLM, use the `/generate_vllm` endpoint:
```bash
curl -X POST http://localhost:8000/generate_vllm \
  -H "Content-Type: application/json" \
  -d '{"prompts": ["Hello, I am", "The weather is", "Once upon a time"]}'
```

## Running Tests

Run the tests in venv with:
```bash
pytest tests/
python -m pytest tests -v
```

## Features

- Basic text generation with single and batch processing
- Streaming response support
- vLLM integration for efficient batched inference
- Comprehensive test coverage 