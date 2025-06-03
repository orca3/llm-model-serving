# Simple LLM Serving Demo

This is a simple demonstration of how to serve a single LLM model using FastAPI. The service uses the facebook/opt-125m model and implements a basic serving architecture with workload management and model execution in a separate process.

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

Send a POST request to `/generate` with a JSON body:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, I am"}'
```

## Running Tests

Run the tests with:
```bash
pytest tests/
``` 