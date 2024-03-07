## Run The Application


create virtual python environment at: serving./venvs/inference_proxy 

cd serving
python -m venv ./venvs/inference_proxy
source ./venvs/inference_proxy/bin/activate

pip install --upgrade pip
pip install -r requirement.txt

deactivate

In commandline, move to the serving folder, run 
`python -m flask run`

If another program is already using port 5000, you’ll see OSError: [Errno 98] or OSError: [WinError 10013] when the server tries to start. See [Address already in use](https://flask.palletsprojects.com/en/3.0.x/server/#address-already-in-use) for how to handle that.

### local debugging

Command line: (1) active environment (2) move to "serving/inference_proxy" folder (3) run `python -m flask run`, which will look for app.py by defult. 

For debuging in VSCode, use the following configuration. Note: make sure to open VSCode at the project root, otherwise change the `"cwd"` to your VSCode root foler.   
```
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

### Docker

build the image
cd serving
docker build . -t orca3ai/serving

check directory structure
docker run -it orca3ai/inference:latest bash

run docker image
docker run --rm -p 8002:80 orca3ai/inference:latest

test
curl http://localhost:8002

[How to Connect to Localhost Within a Docker Container](https://www.howtogeek.com/devops/how-to-connect-to-localhost-within-a-docker-container/)


## Test

https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/

## Build and Deployment Flask app
https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/


## Develop Flask in VSCode 
https://code.visualstudio.com/docs/python/tutorial-flask


## Readings






