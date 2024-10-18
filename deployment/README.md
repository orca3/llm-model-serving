# Setup Instruction
Here are the instructions to deploy/run the lab services on your local computer. 

All the docker images in this repo can be found at [dockerhub/orca3ai](https://hub.docker.com/u/orca3ai).

## Prerequisite 
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (4.27.2 and above) is highly recommended, since it contains docker engine and Docker compose, which are required to run the label. You can also install docker engine and compose separately.   
2. Make sure ports `9020`, `9050`, `9051`, `9052` and `9090` are free on your local computer.

## Installation
The lab is composed of multi-container services, its deployment is managed by docker compose, please refer to [compose.yaml] file for details. To install:
1. Open your terminal and move to `deployment` folder, run 
    ```
    docker-compose up -d
    ```
    We should see all the containers are light up 
    ```sh
    ✔ Container deployment-torchserve-1 started 0.4s
    ✔ Container deployment-inference-1  started 0.4s
    ✔ Container deployment-llm-1        started 0.4s
    ```

2. Check service logs, run 
    ```
    docker-compose logs -f   # Use -f to follow the log output
    ```

3. To stop/restart the containers, you can
    ```
    docker-compose stop | restart
    ``` 
4. Cleanup 
    ```
    docker-compose down -v 
    ```

## Test
We could use the following curl requests to verify the system setup. 

### Verify the inference service is up running
First, verify the proxy (inference) service is up running.
```curl
curl --location 'http://127.0.0.1:9020'
```
We should see `Hello, Inference Service (Flask)!%` in return.

Next, let's try to send a prediction request to the model hosted on the inference service.
```
curl --location 'http://127.0.0.1:9020/image/predict' \
    --form 'img=@egyptian_cat.jpg'
```
We should see `{"class_id":"n02124075","class_name":"Egyptian_cat"}` in return. 

### Verify the torch predictor is up running

First, we verify the resnet model is loaded in the torchserve predictor.
```
curl --location 'http://127.0.0.1:9051/models'
```
We should see the follow json in return.
```json
{
  "models": [
    {
      "modelName": "resnet-152-batch_v2",
      "modelUrl": "resnet-152-batch_v2.mar"
    }
  ]
}
```

Next, let's send a prediction request to the inference service, the service then forwards the request to the torchserve predictor.  
```
curl --location 'http://127.0.0.1:9020/torch/image/predict/resnet-152-batch_v2' \
    --form 'img=@egyptian_cat.jpg'
```
We should see following json object in return.
```json
[
  {
    "Egyptian_cat": 0.9987070560455322
  },
  {
    "snow_leopard": 0.0005450256867334247
  },
  {
    "tabby": 0.0002378501376369968
  },
  {
    "tiger_cat": 0.00020254032278899103
  },
  {
    "lynx": 0.0001917051849886775
  }
]
```

### verify the llm predictor is up and functioning
First, let's call the LLM streaming endpoint, the inference service will forward the request to the llm predictor. 
```sh
curl -N --location 'http://127.0.0.1:9020/llm/stream' \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "What is the capital of USA?"
    }'
```
We should see the following json objects are streamed one by one in return.
```
{"text": "\n", "index": 0, "logprobs": null, "finish_reason": null}
```

Next, let's call LLM predictive endpoint
```sh
curl --location 'http://127.0.0.1:9020/llm/predict' \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "What is the capital of USA?"
    }'
```
We should see the following json object in return.
```json
{
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "logprobs": null,
      "text": "\n kwietno 2015\nCapital of USA\nWashington, D.C., in its entirety, and not just Washington City or"
    }
  ],
  "created": 1713039907,
  "id": "cmpl-4fbc9f39-9821-4830-a32f-922517e04be6",
  "model": "./models/llama/llama-2-7b.Q2_K.gguf",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 32,
    "prompt_tokens": 8,
    "total_tokens": 40
  }
}
```