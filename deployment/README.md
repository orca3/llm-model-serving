# Setup Instruction
Here are the instructions to deploy/run the lab services on your local computer. 

## Prerequisite 
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (4.27.2 and above) is highly recommended, since it contains docker engine and Docker compose, which are required to run the label. You can also install docker engine and compose separately.   
2. Make sure ports `9010`, `9050`, `9051`, `9052` and `9090` are free on your local computer.

## Installation
The lab is composed of multi-container services, its deployment is managed by docker compose, please refer to [compose.yaml] file for details. To install:
1. Open your terminal and move to `deployment` folder, run 
    ```
    docker-compose up -d
    ```
    We should see all the containers are light up 
    [insert picture]

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

```curl

# Verify the inference service is up
curl --location 'http://127.0.0.1:9010'
curl --location 'http://127.0.0.1:9010/image/predict' \
    --form 'img=@egyptian_cat.jpg'


# Verify the torch predictor is up and functioning
curl --location 'http://127.0.0.1:9051/models'
curl --location 'http://127.0.0.1:9010/torch/image/predict/resnet-152-batch_v2' \
    --form 'img=@egyptian_cat.jpg'

# verify the llm predictor is up and functioning
curl --location 'http://127.0.0.1:9010/llm/stream' \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "What is the capital of USA?"
    }'

curl --location 'http://127.0.0.1:9010/llm/predict' \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "What is the capital of USA?"
    }'
```