# Inference service

This is a proxy service which routes the prediction requests to the predictors behind it.

## Run The Application

### Run with docker

First, build docker image
```sh
cd serving
docker build . -t orca3ai/inference
```
Next, run the docker image
```sh
docker run --rm -p 9020:80 -v "$(pwd)"/../models:/home/serving/models orca3ai/inference:latest

docker run --rm -it orca3ai/inference:latest bash # debug
```

Verify the service
```sh
curl http://localhost:9020
```
We should see 
```
Hello, Inference Service (Flask)!
```

### Run locally

First, let's create a virtual python environment (inference_proxy) at: `serving./venvs/inference_proxy` 

```sh
cd serving
python -m venv ./venvs/inference_proxy
source ./venvs/inference_proxy/bin/activate

pip install --upgrade pip
pip install -r requirement.txt

deactivate # de-active the env
```

Next, in commandline, under the serving folder, run the service 
`python -m flask run`

If another program is already using port 5000, you’ll see OSError: [Errno 98] or OSError: [WinError 10013] when the server tries to start. See [Address already in use](https://flask.palletsprojects.com/en/3.0.x/server/#address-already-in-use) for how to handle that.

## Local debug with VSCode

For debuging in VSCode, use the following configuration. 

Note: make sure to open VSCode at the repo root directory(`llm-model-serving`), otherwise change the `"cwd"` to your VSCode root foler.   
```json
{
    "name": "Python Debugger: Flask - Inference Proxy",
    "type": "debugpy",
    "request": "launch",
    "module": "flask",
    "cwd": "${workspaceFolder}/serving/inference_proxy",
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_DEBUG": "1"
    },
    "args": [
        "run",
        "--no-debugger",
        "--no-reload"
    ],
    "jinja": true,
    "autoStartBrowser": false
}
```

<!-- # test llm predict
curl --location 'http://127.0.0.1:9020/llm/predict' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "What is the capital of USA?"
}'

# test llm streaming endpoint
curl --location 'http://127.0.0.1:9020/llm/stream' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "What is the capital of USA?"
}' -->

## Readings
https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/
https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/
https://code.visualstudio.com/docs/python/tutorial-flask









