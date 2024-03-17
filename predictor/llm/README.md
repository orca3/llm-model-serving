
[llama cpp python](https://github.com/abetlen/llama-cpp-python)
[llama cpp]()

```
conda create -n llama-predictor python=3.11
conda activate llama-predictor

conda deactivate
```

Prerequiste on MAC: install XCode
```
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" 
  
pip install llama-cpp-python

pip install -r  requirements.txt
```

Local debugging
```
curl -X POST 'http://localhost:5000/predict?model=llama-2-7b' \
  -H 'Content-Type: application/json' \
  -d "{\"prompt\":\"What is the capital of USA?\"}"

curl -N -X POST http://127.0.0.1:5000/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"What is the capital of USA?\"}" 
  
```

Test the docker image
```
# move the docker context to parent folders (root workspace)
docker build -t orca3ai/llm-predictor ../../ -f ./Dockerfile

docker run -it -p 9090:5000 -e MODEL_DIR="./models/llama" -e HOST_IP="0.0.0.0" -v /Users/chi.wang/workspace/cw/llm-model-serving/models:/usr/src/app/models --rm --name llm-predictor orca3ai/llm-predictor

docker run -it --rm --name llm-predictor orca3ai/llm-predictor bash

docker exec -i -t orca3ai/llm-predictor bash

```

curl -X POST 'http://localhost:9090/predict?model=llama-2-7b' \
  -H 'Content-Type: application/json' \
  -d "{\"prompt\":\"What is the capital of USA?\"}"

curl -N -X POST http://127.0.0.1:9090/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"What is the capital of USA?\"}" 