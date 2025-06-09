# Multi-Model Serving Demo

This is a simple demonstration of a multi-model serving service that manages multiple ML models with limited resources. The service implements a model cache that can hold up to 2 models at a time, loading and unloading models on-demand based on usage patterns.

## Features

- On-demand model loading
- LRU (Least Recently Used) model caching
- Support for different model types (text and image)
- Generic API interface for different model inputs
- Model metadata management
- Framework-specific model workers (Transformers, TorchVision)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── server.py      # FastAPI server and endpoints
│   ├── store.py       # Model metadata management
│   ├── manager.py     # Model caching and lifecycle
│   ├── engine.py      # Model worker factory and management
│   └── worker.py      # Abstract worker and framework-specific implementations
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

## Triton Server Setup

To run the tests with Triton Inference Server:

1. Create a model repository directory structure:
```bash
mkdir -p model_dir/densenet_onnx/1
```

2. Copy your ONNX model to the repository:
```bash
cp path/to/your/model.onnx model_dir/densenet_onnx/1/
```

3. Create a model configuration file `model_dir/densenet_onnx/config.pbtxt`:
```protobuf
name: "densenet_onnx"
platform: "onnxruntime_onnx"
max_batch_size: 0
input [
  {
    name: "data_0"
    data_type: TYPE_FP32
    dims: [ 3, 224, 224 ]
  }
]
output [
  {
    name: "fc6_1"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]
```

4. Another way to get the model files are: 
```bash
git clone -b r25.05 https://github.com/triton-inference-server/server.git
cd server/docs/examples
./fetch_models.sh
```

5. Start Triton server with explicit model control:
```bash
# Using Docker (recommended)
docker run -p8009:8000 -p8010:8001 -p8011:8002 \
    -v $(pwd)/model_dir:/models \
    nvcr.io/nvidia/tritonserver:24.12-py3 \
    tritonserver --model-repository=/models --model-control-mode=explicit

# Or using tritonserver directly
tritonserver --model-repository=./model_dir --model-control-mode=explicit
```

6. Run the tests:
```bash
python -m unittest tests/test_triton_densenet.py
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
  -d '{"model_id": "550e8400-e29b-41d4-a716-446655440000", "input_data": "This movie was great!"}'
```

For spam detection:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"model_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8", "input_data": "Win a free iPhone now!"}'
```

For image classification:
```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"model_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7", "input_data": "path/to/image.jpg"}'
```

## Architecture

The service consists of five main components:

1. **Server** (`server.py`): Provides HTTP endpoints for model predictions
2. **Store** (`store.py`): Manages model metadata and configurations
3. **Manager** (`manager.py`): Handles model caching and lifecycle
4. **Engine** (`engine.py`): Factory for creating and managing model workers based on framework type
5. **Worker** (`worker.py`): Abstract base class and framework-specific implementations for model inference
   - `ModelWorker`: Abstract base class defining the interface
   - `TransformerWorker`: Handles transformer-based models
   - `TorchVisionWorker`: Handles torchvision-based models

The service automatically manages model loading and unloading based on usage patterns, ensuring efficient resource utilization. The architecture follows the Factory pattern for worker creation and the Strategy pattern for framework-specific implementations. 