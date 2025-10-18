# vLLM Model Optimization Notebook Setup Guide

This guide will help you set up a local development environment to run the `model_optimization_in_practice.ipynb` notebook, which demonstrates vLLM performance optimization techniques including quantization, caching, and benchmarking.

>
**Note:** The `model_optimization_in_practice.ipynb` notebook requires GPU and it is designed to run best with the vLLM code base directly. To ensure maximum compatibility and ease of use, **please set up the vLLM development environment as described below, then copy the `model_optimization_in_practice.ipynb` notebook and any related helper scripts (such as `inspect_dataset.py`) into the root of your `vllm` repository folder.**  
>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Running the Notebook](#running-the-notebook)
- [Understanding the Results](#understanding-the-results)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)


## A quick setup overview

1. **Set up your development environment** (see instructions in this guide).
2. **Copy notebook and helper scripts:**
    ```bash
    cp /path/to/model_optimization_in_practice.ipynb /path/to/vllm/
    cp /path/to/inspect_dataset.py /path/to/vllm/
    # ...copy any other utility files as needed
    ```
3. **Change directory to your vllm repo:**
    ```bash
    cd /path/to/vllm/
    ```
4. **Activate your venv** and **launch Jupyter:**
    ```bash
    source .venv/bin/activate
    jupyter lab  # or jupyter notebook
    ```
5. **Within Jupyter**, open and run `model_optimization_in_practice.ipynb`.

This arrangement ensures that any code inside the notebook can directly import from the local vllm codebase (without needing pip installation) and that helper scripts (like `inspect_dataset.py`) are accessible in your notebook environment.

## Prerequisites

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (L40S, A100, H100, RTX 40-series recommended)
- **VRAM**: Minimum 24GB GPU memory for Qwen3-14B models (46GB+ recommended for optimal performance)
- **RAM**: 32GB+ system RAM
- **Storage**: 100GB+ free space for models and datasets

### Software Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.8-3.12 (3.12 recommended for best performance)
- **CUDA**: 11.8+ or 12.1+
- **Git**: For cloning the repository
- **uv**: Fast Python package installer (will be installed automatically)

## Environment Setup

### 1. Clone vLLM Repository

```bash
# Clone the vLLM repository
git clone https://github.com/vllm-project/vllm.git
cd vllm

# Optional: Checkout a specific version for stability
git checkout v0.6.0  # or latest stable version
```

### 2. Create Virtual Environment with uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment with Python 3.12 and seed packages
uv venv --python 3.12 --seed

# Activate the virtual environment
source .venv/bin/activate
```

**Note**: `uv` is a fast Python package installer and resolver. The `--seed` flag pre-installs common packages (pip, setuptools, wheel) for faster subsequent installations.

### 3. Install vLLM in Development Mode with uv

```bash
# Install vLLM in editable mode with precompiled dependencies using uv
# VLLM_USE_PRECOMPILED=1 forces use of precompiled wheels for faster installation
VLLM_USE_PRECOMPILED=1 uv pip install -e .

# Install additional dependencies for the notebook and testing
uv pip install jupyter matplotlib numpy requests pytest tblib
```

**Benefits of using uv:**
- **Faster installation**: 10-100x faster than pip
- **Better dependency resolution**: More reliable dependency management
- **Precompiled wheels**: `VLLM_USE_PRECOMPILED=1` automatically uses precompiled packages
- **No compilation needed**: Avoids building PyTorch and CUDA extensions from source

### 4. Verify Installation

```bash
# Check vLLM installation
python -c "import vllm; print(f'vLLM version: {vllm.__version__}')"

# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import torch; print(f'CUDA devices: {torch.cuda.device_count()}')"
```

### 5. Download Required Datasets

```bash
# Create datasets directory
mkdir -p datasets

# Download ShareGPT dataset (used in benchmarks)
# This is a large file (~1.5GB), so it may take several minutes
wget -O datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
    "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"

# Verify dataset download
ls -lh datasets/ShareGPT_V3_unfiltered_cleaned_split.json
# Should show file size ~650MB

# Alternative: Use curl if wget is not available
curl -L -o datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
    "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"
```

**Dataset Information:**
- **ShareGPT**: Real conversation data for realistic benchmarking
- **Size**: ~650MB, contains thousands of conversation examples
- **Format**: JSON with conversation pairs (human/assistant)
- **Use Case**: Tests model performance on diverse, real-world conversations

### 6. Examine Dataset Structure

You can use the included `inspect_dataset.py` script to examine and validate datasets:

First copy the `inspect_dataset.py` to `vllm` folder and run the following command.  

```bash
# Basic dataset inspection
python inspect_dataset.py --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json --model Qwen/Qwen3-14B --num-prompts 100

# Inspect prefix repetition dataset
python inspect_dataset.py --dataset-name prefix_repetition --model Qwen/Qwen3-14B --num-prompts 50 --prefix-repetition-prefix-len 256 --prefix-repetition-suffix-len 256 --prefix-repetition-num-prefixes 5 --prefix-repetition-output-len 128

# Save samples to file for detailed inspection
python inspect_dataset.py --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json --model Qwen/Qwen3-14B --num-prompts 100 --save-samples

# Inspect random dataset with custom parameters
python inspect_dataset.py --dataset-name random --model Qwen/Qwen3-14B --num-prompts 50 --random-input-len 512 --random-output-len 64 --random-prefix-len 128
```

**What the inspect script shows:**
- **Dataset Overview**: Total number of samples
- **Length Distributions**: Min/max/mean/median/std for prompt and output lengths
- **Sample Prompts**: First 5 samples with truncated content
- **Length Histogram**: Visual distribution of prompt lengths
- **Optional**: Save samples to JSON file for detailed analysis

**Example Output:**
```
=== Dataset Overview ===  
Total samples: 100  

=== Prompt Length Distribution ===  
Min prompt length: 5  
Max prompt length: 817  
Mean prompt length: 232.60  
Median prompt length: 141.50  
Std prompt length: 241.42  

=== Output Length Distribution ===  
Min output length: 4  
Max output length: 771  
Mean output length: 220.61  
Median output length: 164.50  
Std output length: 210.23  

=== Sample Prompts ===  
--- Sample 1 ---  
Prompt length: 8  
Output length: 5  
Request ID: benchmark-serving0  
Prompt:  
Hi! Can you explain what reinforcement learning is?

--- Sample 2 ---  
Prompt length: 12  
Output length: 11  
Request ID: benchmark-serving1  
Prompt:  
Give me a code example of a for loop in Python.

--- Sample 3 ---  
Prompt length: 341  
Output length: 197  
Request ID: benchmark-serving2  
Prompt:  
<truncated prompt...>

--- Sample 4 ---  
Prompt length: 783  
Output length: 725  
Request ID: benchmark-serving3  
Prompt:  
<truncated prompt...>

--- Sample 5 ---  
Prompt length: 5  
Output length: 4  
Request ID: benchmark-serving4  
Prompt:  
Hello!

=== Prompt Length Histogram ===  
   5-  95 tokens: *********************************************  
  95- 185 tokens: ********  
 185- 275 tokens: *********  
 275- 365 tokens: **************  
 365- 456 tokens: *****  
 456- 546 tokens: *****  
 546- 636 tokens: ****  
 636- 726 tokens: ***  
 726- 817 tokens: *******  
```

**Dataset Examination Benefits:**
- **Validation**: Ensure dataset downloaded correctly and has expected structure
- **Length Analysis**: Understand prompt/output length distributions for optimization
- **Content Preview**: See actual prompts to understand dataset quality
- **Parameter Tuning**: Use statistics to optimize benchmark parameters
- **Debugging**: Identify issues with dataset loading or content

## Running the Notebook

### 1. Start Jupyter Notebook

```bash
# Make sure you're in the vllm directory with virtual environment activated
cd /path/to/vllm
source .venv/bin/activate

# Start Jupyter notebook
jupyter notebook
```

### 2. Open the Notebook

Navigate to `model_optimization_in_practice.ipynb` in your browser and open it.


## Optional: Use VS Code Remote SSH for Development

Instead of working through the Jupyter web UI alone with your local GPU, you can use cloud vendor server, such as AWS EC2 (g6e or p4d), and use VS Code and [VS Code Remote SSH](https://code.visualstudio.com/docs/remote/ssh) to connect directly to your EC2 instance, open the `vllm` folder, and fully inspect, debug, and run code. This allows for easier editing, testing, and interactive debugging.

### Steps to Connect with VS Code SSH
After you setup your EC2 server, you can

1. **Ensure SSH Access:**
   Make sure you have your EC2 SSH key and can `ssh` into your instance:
   ```bash
   ssh -i /path/to/key.pem ubuntu@<your-ec2-public-ip>
   ```

2. **Open VS Code and Install Remote SSH Extension:**
   - Install the "Remote - SSH" extension from Microsoft in VS Code.
   - Click the green bottom-left "><" icon and choose "Remote-SSH: Connect to Host...". Enter your connection details, e.g.:
     ```
     ubuntu@<your-ec2-public-ip>
     ```
   - When prompted, select your key file if needed.

3. **Open the vllm Folder:**
   - In the VS Code remote session, use "File > Open Folder..." and select `/path/to/vllm` (where you cloned your repo).
   - Open an integrated terminal (`Ctrl+Backtick` or via menu), and activate your virtual environment:
     ```bash
     source .venv/bin/activate
     ```

4. **(Optional) Copy the Notebook to the vllm Folder:**
   - If your notebook is outside the `vllm` folder, move or copy it for easier access:
     ```bash
     cp /path/to/model_optimization_in_practice.ipynb /path/to/vllm/
     ```

5. **Launch and Use the Notebook in VS Code:**
   - Open `model_optimization_in_practice.ipynb` via VS Code. You can run cells directly and interact with your vLLM code, all in a single debugging environment.
   - Set breakpoints in Python files, open any code in the `vllm` repo, and run/edit/debug with the remote Python interpreter.

This workflow is very useful for development: you can edit datasets, modify vLLM code, run server or benchmark scripts, and debug issues, all within VS Code as if you were working locally.


### 3. Run the Notebook Cells

The notebook is organized into phases, you can just follow through. 

### Key Metrics Explained

- **Request Throughput**: Requests completed per second
- **Output Throughput**: Output tokens generated per second
- **Total Token Throughput**: Combined input + output tokens per second
- **TTFT (Time to First Token)**: Latency until first token generation
- **TPOT (Time Per Output Token)**: Average time per output token
- **ITL (Inter-Token Latency)**: Time between consecutive tokens

## Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory
```bash
# Error: CUDA out of memory
# Solution: Reduce model size, reserved GPU memory, or use quantization
vllm serve Qwen/Qwen3-14B-AWQ --quantization awq --gpu-memory-utilization 0.8
```

#### 2. Ray Placement Group Issues
```bash
# Error: Cannot create placement group
# Solution: Use single GPU or reduce tensor parallel size
vllm serve Qwen/Qwen3-14B-AWQ --tensor-parallel-size 1
```

#### 3. Model Download Issues
```bash
# Error: Model not found
# Solution: Set HuggingFace token or use local model path
export HUGGINGFACE_HUB_TOKEN="your_token_here"
```

#### 4. Port Already in Use
```bash
# Error: Port 8000 already in use
# Solution: Kill existing processes or use different port
pkill -f "vllm serve"
# Or use different port
vllm serve --port 8001
```

#### 5. Dataset Not Found
```bash
# Error: ShareGPT dataset not found
# Solution: Download the dataset manually
wget -O ShareGPT_V3_unfiltered_cleaned_split.json \
    "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"
```

#### 6. Dataset Loading Issues
```bash
# Error: Dataset loading fails or returns empty results
# Solution: Validate dataset and test loading mechanisms

# Check dataset file integrity
ls -lh datasets/ShareGPT_V3_unfiltered_cleaned_split.json
file datasets/ShareGPT_V3_unfiltered_cleaned_split.json

# Test dataset loading with the test framework
python -m pytest tests/plugins_tests/test_platform_plugins.py::test_platform_plugins -v

# Validate JSON structure
python -c "
import json
with open('datasets/ShareGPT_V3_unfiltered_cleaned_split.json', 'r') as f:
    data = json.load(f)
print(f'Dataset entries: {len(data)}')
print(f'Sample keys: {list(data[0].keys()) if data else \"Empty dataset\"}')
"
```

#### 7. Build/Compilation Issues
```bash
# Error: Long build times or compilation failures
# Solution: Use uv with precompiled dependencies

# Clear uv cache and reinstall with precompiled wheels
uv cache clean
VLLM_USE_PRECOMPILED=1 uv pip install -e .

# Alternative: Use traditional pip with precompiled wheels
pip cache purge
pip install -e . --find-links https://download.pytorch.org/whl/torch_stable.html

# Check if compilation is needed
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import torch; print(f'CUDA version: {torch.version.cuda}')"
```

#### 8. Missing Test Dependencies
```bash
# Error: ModuleNotFoundError: No module named 'tblib'
# Solution: Install missing test dependencies

# Install tblib and other test dependencies
uv pip install tblib pytest-xdist pytest-asyncio

# Or install all test dependencies at once
uv pip install jupyter matplotlib numpy requests pytest tblib pytest-xdist pytest-asyncio

# Verify test framework works
python -m pytest tests/plugins_tests/test_platform_plugins.py::test_platform_plugins -v
```

### Debugging Commands

```bash
# Check GPU status
nvidia-smi

# Check vLLM processes
ps aux | grep vllm

# Check server health
curl http://localhost:8000/health

# Check server models
curl http://localhost:8000/v1/models

# Monitor GPU usage
watch -n 1 nvidia-smi

# Check logs
tail -f vllm.log

# Dataset debugging commands
ls -la datasets/
file datasets/ShareGPT_V3_unfiltered_cleaned_split.json
head -n 5 datasets/ShareGPT_V3_unfiltered_cleaned_split.json

# Inspect dataset structure and content
python inspect_dataset.py --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json --model Qwen/Qwen3-14B --num-prompts 50

# Test dataset loading
python -c "
import sys
sys.path.insert(0, '.')
from vllm.benchmarks.datasets import ShareGPTDataset
dataset = ShareGPTDataset()
print('Dataset loaded successfully')
"

# Run test framework for dataset validation
python -m pytest tests/plugins_tests/test_platform_plugins.py::test_platform_plugins -v
```

## Advanced Configuration

### Benchmark Configuration Examples

#### High Throughput Benchmark
```bash
vllm bench serve \
    --backend vllm \
    --base-url "http://localhost:8000" \
    --dataset-name sharegpt \
    --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json \
    --num-prompts 1000 \
    --request-rate 50 \
    --max-concurrency 50 \
    --save-result \
    --result-filename high_throughput_results.txt \
    --model Qwen/Qwen3-14B-AWQ
```

#### Prefix Repetition Benchmark
```bash
vllm bench serve \
    --backend vllm \
    --base-url "http://localhost:8000" \
    --dataset-name prefix_repetition \
    --num-prompts 1000 \
    --request-rate 10 \
    --prefix-repetition-prefix-len 256 \
    --prefix-repetition-suffix-len 256 \
    --prefix-repetition-num-prefixes 10 \
    --prefix-repetition-output-len 128 \
    --max-concurrency 20 \
    --save-result \
    --result-filename prefix_repetition_results.txt \
    --model Qwen/Qwen3-14B-AWQ
```

### Development Workflow

#### Making Changes to vLLM Code
```bash
# After making changes to vLLM source code
VLLM_USE_PRECOMPILED=1 uv pip install -e .  # Reinstall in editable mode with uv

# Alternative: Use traditional pip
pip install -e .  # Reinstall in editable mode

# Restart the server to pick up changes
pkill -f "vllm serve"
# Then restart with your configuration
```

#### Testing Custom Datasets
```bash
# Create custom dataset in vllm/benchmarks/datasets.py
# Test your dataset
vllm bench serve \
    --dataset-name your_custom_dataset \
    --num-prompts 100 \
    --request-rate 5 \
    --save-result \
    --result-filename custom_dataset_results.txt
```

#### Examining Dataset Loading with Test Framework
```bash
# Use the test framework to examine dataset loading mechanisms
python -m pytest tests/plugins_tests/test_platform_plugins.py::test_platform_plugins -v -s

# Use inspect_dataset.py for comprehensive dataset analysis
python inspect_dataset.py --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json --model Qwen/Qwen3-14B --num-prompts 100 --save-samples

# Test specific dataset classes
python -c "
import sys
sys.path.insert(0, '.')
from vllm.benchmarks.datasets import ShareGPTDataset, PrefixRepetitionRandomDataset

# Test ShareGPT dataset
sharegpt = ShareGPTDataset()
print(f'ShareGPT dataset: {sharegpt.__class__.__name__}')

# Test prefix repetition dataset
prefix_rep = PrefixRepetitionRandomDataset(random_seed=42)
print(f'Prefix repetition dataset: {prefix_rep.__class__.__name__}')

# Test dataset sampling
from vllm.transformers_utils.tokenizer import get_tokenizer
tokenizer = get_tokenizer('Qwen/Qwen3-14B', tokenizer_mode='auto')
requests = prefix_rep.sample(tokenizer=tokenizer, num_requests=5, prefix_len=128, suffix_len=128, num_prefixes=2, output_len=64)
print(f'Generated {len(requests)} sample requests')
print(f'First request prompt length: {requests[0].prompt_len}')
"
```

#### Debugging Dataset Issues
```bash
# Check if dataset files exist and are readable
ls -la datasets/
file datasets/ShareGPT_V3_unfiltered_cleaned_split.json

# Validate JSON format
python -c "
import json
try:
    with open('datasets/ShareGPT_V3_unfiltered_cleaned_split.json', 'r') as f:
        data = json.load(f)
    print(f'✅ JSON is valid, contains {len(data)} entries')
except Exception as e:
    print(f'❌ JSON validation failed: {e}')
"

# Test dataset loading with verbose output
python -c "
import sys
sys.path.insert(0, '.')
import logging
logging.basicConfig(level=logging.DEBUG)

from vllm.benchmarks.datasets import ShareGPTDataset
dataset = ShareGPTDataset()
print('Dataset loaded successfully')
"
```

## Contributing

When making changes to vLLM for this notebook:

1. **Test your changes**: Run the notebook end-to-end
2. **Update benchmarks**: Add new benchmark configurations if needed
3. **Document changes**: Update this README with new features
4. **Performance validation**: Ensure changes don't regress performance

## Quick Reference

### Essential Commands

```bash
# Setup (run once)
git clone https://github.com/vllm-project/vllm.git && cd vllm
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv
uv venv --python 3.12 --seed && source .venv/bin/activate
VLLM_USE_PRECOMPILED=1 uv pip install -e .
uv pip install jupyter matplotlib numpy requests pytest tblib

# Download dataset
mkdir -p datasets
wget -O datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
    "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"

# Start server
vllm serve Qwen/Qwen3-14B-AWQ --quantization awq --port 8000

# Run benchmark
vllm bench serve --backend vllm --base-url "http://localhost:8000" \
    --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
    --num-prompts 1000 --request-rate 10 --max-concurrency 20 \
    --save-result --result-filename results.txt

# Test dataset loading
python -m pytest tests/plugins_tests/test_platform_plugins.py::test_platform_plugins -v

# Inspect dataset structure
python inspect_dataset.py --dataset-name sharegpt --dataset-path datasets/ShareGPT_V3_unfiltered_cleaned_split.json --model Qwen/Qwen3-14B --num-prompts 50
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Long build times | Use `VLLM_USE_PRECOMPILED=1 uv pip install -e .` |
| Dataset not found | Download with `wget` or `curl` to `datasets/` directory |
| CUDA OOM | Use `--quantization awq` and `--gpu-memory-utilization 0.8` |
| Port in use | `pkill -f "vllm serve"` or use `--port 8001` |
| Ray placement group | Use `--tensor-parallel-size 1` |
| uv not found | Install with `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Missing tblib | Run `uv pip install tblib pytest-xdist pytest-asyncio` |

## Support

- **vLLM Documentation**: https://docs.vllm.ai/
- **vLLM GitHub Issues**: https://github.com/vllm-project/vllm/issues
- **HuggingFace Models**: https://huggingface.co/Qwen

---

**Note**: This setup is optimized for development and testing. For production deployments, consider additional security, monitoring, and scaling configurations.
