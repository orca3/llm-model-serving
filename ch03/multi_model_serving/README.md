# Multi-Model Serving Demo

This is a simple demonstration of a multi-model serving service that manages multiple ML models with limited resources. The service implements a model cache that can hold up to 2 models at a time, loading and unloading models on-demand based on usage patterns.

## Features

- On-demand model loading
- LRU (Least Recently Used) model caching
- Support for different model types (text and image)
- Generic API interface for different model inputs
- Model metadata management

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── server.py      # FastAPI server and endpoints
│   ├── store.py       # Model metadata management
│   ├── manager.py     # Model caching and lifecycle
│   └── worker.py      # Model loading and inference
├── config/
│   └── models.json    # Model configurations
└── requirements.txt   # Project dependencies
```

## Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
# Run with default port (8001)
python -m app.server

# Or specify a custom port
PORT=8002 python -m app.server
```

## API Usage

### List Available Models
```bash
curl http://localhost:8001/models
```

### Make Predictions

For text models (sentiment analysis):
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"model_id": "sentiment", "input_data": "This movie was great!"}'
```

For spam detection:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"model_id": "spam", "input_data": "Win a free iPhone now!"}'
```

For image classification:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"model_id": "image", "input_data": "path/to/image.jpg"}'
```

## Architecture

The service consists of four main components:

1. **Server** (`server.py`): Provides HTTP endpoints for model predictions
2. **Store** (`store.py`): Manages model metadata and configurations
3. **Manager** (`manager.py`): Handles model caching and lifecycle
4. **Worker** (`worker.py`): Executes model inference

The service automatically manages model loading and unloading based on usage patterns, ensuring efficient resource utilization. 