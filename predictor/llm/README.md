# LLM Predictor
This is a sample predictor for demoing how to host a generative large language model. 

In order to run the example without GPU, we choose llama-2-7b model with [llama cpp python](https://github.com/abetlen/llama-cpp-python) serving framework. 

We provide two examples in this LLM predictor: 
* Streaming api: returns token as soon as the model produces it.
* Predictive api: returns the entire generated content all at once.

## Prerequisite
1. Make sure port 9090 is not occupied.
2. Please check whether `llama-2-7b.Q2_K.gguf` exists in the `llm-model-serving/models/llm` folder. If not, please follow the instructions in [download.md](../../models/llama/download.md) to download it. 

## Run the LLM predictor docker locally

First, move to the `llm-model-serving/predictor/llm` directory and build the docker image.
```docker
docker build -t orca3ai/llm-predictor ../../ -f ./Dockerfile # "../../" sets the docker context to parent folders (repo root)
```

Next, launch the docker image
```docker 
docker run --rm -it -p 9090:5000 \
  -e MODEL_DIR="./models/llama" \
  -e HOST_IP="0.0.0.0" \
  -v $(pwd)/../../models:/usr/src/app/models \
  --name llm-predictor \
  orca3ai/llm-predictor
```

Now, let's verify the predictor with a few queries:

1. Predictive query for "What is the capital of USA?"
  ```
  curl -X POST 'http://localhost:9090/predict?model=llama-2-7b' \
    -H 'Content-Type: application/json' \
    -d "{\"prompt\":\"What is the capital of USA?\"}"
  ```

  We should see return json object like below 
  ```json
    {
    "choices": [
      {
        "finish_reason": "length",
        "index": 0,
        "logprobs": null,
        "text": "\n kwietnik 07, 2018\nWashington DC is not only a capital city of America. In Washington DC, you can see"
      }
    ],
    "created": 1712989683,
    "id": "cmpl-1092f838-14e8-4534-a7db-d87daf93dfcd",
    "model": "./models/llama/llama-2-7b.Q2_K.gguf",
    "object": "text_completion",
    "usage": {
      "completion_tokens": 32,
      "prompt_tokens": 8,
      "total_tokens": 40
    }
  }
  ```

2. Streaming query for "What is the capital of USA?"
  ```curl
  curl -N -X POST http://127.0.0.1:9090/stream \
    -H "Content-Type: application/json" \
    -d "{\"prompt\":\"What is the capital of USA?\"}" 
  ```

  We should see below token json object returned one at a time:
  ```json
  {"text": "\n", "index": 0, "logprobs": null, "finish_reason": null}
  ```

3. Clean up
  ```docker 
  docker stop llm-predictor
  ```

4. Troubleshooting
  ```docker
  docker run -it --rm --name llm-predictor orca3ai/llm-predictor bash

  docker exec -i -t orca3ai/llm-predictor bash
  ```

## Dev environment setup
In this section, we talk about how to run and debug the llm predictor locally.

First, create a python virtual environment - `llama-predictor`.
```sh
conda create -n llama-predictor python=3.11
conda activate llama-predictor

conda deactivate
```

After creating env, install the prerequisites for [llama cpp python](https://github.com/abetlen/llama-cpp-python) in this virtual env (`llama-predictor`). For mac, install XCode; For linux, install gcc or clang.

Next, install the llama-cpp package and other packages.
```sh
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" 
pip install llama-cpp-python
pip install -r  requirements.txt
```

Run and debug the code in VSCode following configuration (launch.json), remember to open VSCode at the `llm-model-serving/predictor/llm` directory. 

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

After the predictor is running, we can use following curl command to test the predictive and streaming api.
```
curl -X POST 'http://localhost:5000/predict?model=llama-2-7b' \
  -H 'Content-Type: application/json' \
  -d "{\"prompt\":\"What is the capital of USA?\"}"

curl -N -X POST http://127.0.0.1:5000/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"What is the capital of USA?\"}" 
  
```