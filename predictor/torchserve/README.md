Torch serve example from: [Batch Inference with TorchServe](https://github.com/pytorch/serve/blob/master/docs/batch_inference_with_ts.md)


Run the following command under `serving` folder. 
```docker run --rm -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:8081:8081 -p 127.0.0.1:8082:8082 --name torchserve -v $(pwd)/models:/home/model-server/model-store pytorch/torchserve:0.1.1-cpu```

Check current loaded models
curl localhost:8081/models

no model loaded

Register model 
$ curl -X POST "localhost:8081/models?url=https://torchserve.pytorch.org/mar_files/resnet-152-batch_v2.mar&batch_size=3&max_batch_delay=10&initial_workers=1"

$ curl -X POST "localhost:8081/models?url=resnet-152-batch_v2.mar&batch_size=3&max_batch_delay=10&initial_workers=1"

Update model setting
curl -v -X PUT "http://localhost:8081/models/resnet-152-batch_v2?max_worker=3&batch_size=4"

check model settings (describe model)
curl http://localhost:8081/models/resnet-152-batch_v2

Use configuration file [config.properties](config.properties)
docker run --rm -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:8081:8081 -p 127.0.0.1:8082:8082 --name torchserve -v $(pwd)/models:/home/model-server/model-store -v $(pwd)/../predictor/torchserve/config.properties:/home/model-server/config.properties pytorch/torchserve:0.1.1-cpu

Troubleshoot
docker exec -it torchserve bash