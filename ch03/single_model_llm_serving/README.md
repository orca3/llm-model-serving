# Simple LLM Serving Demo

This is a simple demonstration of how to serve a single LLM model using FastAPI. The service uses the facebook/opt-125m model and implements a basic serving architecture with workload management and model execution in a separate process. It also includes vLLM integration for efficient batched inference.

## Architecture Overview

The system is designed with a modular architecture that separates concerns across different components:

### Core Components

#### 1. **main.py (API Layer)**
- **Responsibility**: HTTP API endpoints and request/response handling
- **Key Functions**:
  - Exposes REST API endpoints (`/basic_generate`, `/generate`, `/generate_stream`, `/generate_vllm`)
  - Handles request validation using Pydantic models
  - Manages FastAPI application lifecycle and dependency injection
  - Provides both synchronous and streaming response capabilities

#### 2. **LLMEngine Class** (`llm/llm.py`)
- **Responsibility**: High-level orchestration and client interface
- **Key Functions**:
  - Coordinates between WorkloadManager and ModelExecutor
  - Manages the continuous processing loop for streaming requests
  - Provides both traditional and vLLM-based generation methods
  - Handles async streaming with proper queue management
  - Manages model lifecycle and cleanup

#### 3. **WorkloadManager** (`llm/workload_manager.py`)
- **Responsibility**: Request queuing and batch management
- **Key Functions**:
  - Manages incoming request queues (separate for streaming and batch)
  - Implements batching logic to optimize throughput
  - Tracks active sequences and their states
  - Handles request lifecycle from creation to completion
  - Supports both streaming and non-streaming workloads

#### 4. **ModelExecutor** (`llm/model_executor.py`)
- **Responsibility**: Process management and model execution coordination
- **Key Functions**:
  - Manages separate worker processes for model inference
  - Handles inter-process communication via queues
  - Coordinates between main process and model worker
  - Supports both batch and streaming execution modes

#### 5. **ModelWorker** (`llm/model_worker.py`)
- **Responsibility**: Model inference execution in separate process
- **Key Functions**:
  - Runs in a separate process for isolation
  - Handles actual model inference using transformers
  - Manages model state and token generation
  - Supports both batch and streaming token generation
  - Handles device management (CPU/GPU)

#### 6. **ModelManager** (`llm/model_manager.py`)
- **Responsibility**: Model loading and caching
- **Key Functions**:
  - Loads and caches transformer models and tokenizers
  - Manages model storage and retrieval
  - Handles model initialization and configuration

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

### Streaming Generation
For real-time token streaming:
```bash
curl -X POST http://localhost:8000/generate_stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, I am"}' \
  --no-buffer
```

## Running Tests

Run the tests with:
```bash
pytest tests/ -v
```

Or run specific test files:
```bash
python -m pytest tests/test_vllm.py -v
python -m pytest tests/test_api.py -v
```

## Features

- **Multi-modal Generation**: Basic text generation with single and batch processing
- **Streaming Support**: Real-time token streaming with Server-Sent Events
- **vLLM Integration**: High-performance batched inference using vLLM
- **Process Isolation**: Model execution in separate processes for stability
- **Workload Management**: Intelligent batching and queue management
- **Comprehensive Testing**: Full test coverage for all endpoints and functionality

## Architecture Benefits

- **Scalability**: Separate processes allow for better resource utilization
- **Reliability**: Process isolation prevents model crashes from affecting the API
- **Performance**: Batching and vLLM integration optimize throughput
- **Flexibility**: Support for both streaming and batch processing modes 