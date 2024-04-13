# Torchserve Predictor

A example for how to use torchserve image to serve resnet model. This sample is extended from: [Batch Inference with TorchServe](https://github.com/pytorch/serve/blob/master/docs/batch_inference_with_ts.md)

Note: Please ensure port `9050`, `9051`, `9052` are not occupied. Now, let's run the torchserve container locally.

## Local setup and test

1. Move to the `root (llm-model-serving)` folder and run:
    ```docker
    docker run --rm -it \
        -p 127.0.0.1:9050:8080 \
        -p 127.0.0.1:9051:8081 \
        -p 127.0.0.1:9052:8082 \
        --name torchserve \
        -v $(pwd)/models:/home/model-server/model-store \
        pytorch/torchserve:0.1.1-cpu
    ```
    We should see following logs indicates the torchserve container is running
    ```
    2024-04-13 05:04:13,918 [INFO ] main org.pytorch.serve.ModelServer -
    ```

2. Query torchserve to check current loaded models
    ```curl
    curl localhost:9051/models
    ```
    We should see there are no model hosted:
    ```json
    {
        "models": []
    }
    ```

3. Let's register a model and specify serving resources. Note: this may take a while since it needs download the model. 

    ```curl
    curl -X POST "localhost:9051/models?url=https://torchserve.pytorch.org/mar_files/resnet-152-batch_v2.mar&batch_size=3&max_batch_delay=10&initial_workers=1"
    ```

    <!-- $ curl -X POST "localhost:9051/models?url=resnet-152-batch_v2.mar&batch_size=3&max_batch_delay=10&initial_workers=1" -->

    We could also update the model setting
    ```curl
    curl -v -X PUT "http://localhost:9051/models/resnet-152-batch_v2?max_worker=3&batch_size=4"
    ```

    Check model settings (describe model)
    ```
    curl http://localhost:9051/models/resnet-152-batch_v2
    ```

4. We could also use configuration file [config.properties](config.properties) to preload models when starts the docker container:
    ```docker
    docker run --rm -it \
        -p 127.0.0.1:9050:8080 \
        -p 127.0.0.1:9051:8081 \
        -p 127.0.0.1:9052:8082 \
        --name torchserve \
        -v $(pwd)/models:/home/model-server/model-store \
        -v $(pwd)/predictor/torchserve/config.properties:/home/model-server/config.properties \
        pytorch/torchserve:0.1.1-cpu
    ```

5. For troubleshoot, we could run ssh to the docker container:
    ```docker
    docker exec -it torchserve bash
    ```

6. Clean up
    ```docker
    docker stop torchserve
    ```