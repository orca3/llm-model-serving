from inference.app import app
from flask import jsonify, request, Response
import os

import requests

torchserve_host = "torchserve-predictor"
llm_host = "llm-predictor"

@app.route('/torch/image/predict', defaults={'model_name': None}, methods=['POST'])
@app.route('/torch/image/predict/<model_name>', methods=['POST'])
def torch_predict(model_name):
    # route prediction request to torch serve predictor
    # torch serve inference rest api: https://pytorch.org/serve/inference_api.html
    
    if not model_name:
        model_name = "resnet-152-batch_v2"
        
    host = torchserve_host+":8080" if 'PREDICTOR_TYPE' in os.environ else "localhost:9050"
    domain = "http://{0}".format(host)
    
    res = requests.get(
        url="{0}/predictions/{1}".format(domain, model_name), 
        data=request.files['img'])
        
    return res.content

@app.route('/torch/models/{model}', methods=['GET'])
def torch_list_models(model):
    
    host = torchserve_host+":8081" if 'PREDICTOR_TYPE' in os.environ else "localhost:9051"
    domain = "http://{0}".format(host)
    
    res = requests.get("{0}/models".format(domain))
    return res.content
   
   
@app.route("/llm/stream", methods=['POST'])
def llm_stream():
    data = request.get_json()
    prompt = data['prompt']
    
    host = llm_host+":5000" if 'PREDICTOR_TYPE' in os.environ else "localhost:9090"
    url = "http://{0}/stream".format(host)
    
    response = requests.post(
        url,
        stream=True,
        json= {"prompt": prompt}
    )
    
    def generate():
        try:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    yield chunk
        except Exception as e:
            print("Error streaming content: {0}".format(str(e)))
        finally:
            response.close()

    # Create a streamed response with the generator and return it
    return Response(generate(), content_type=response.headers['Content-Type'])

@app.route('/llm/predict', methods=['POST'])
def llm_predict():
       
    data = request.get_json()
    prompt = data['prompt']
    
    host = llm_host+":5000" if 'PREDICTOR_TYPE' in os.environ else "localhost:9090"
    url = "http://{0}/predict".format(host)
    
    try:
        response = requests.post(
            url,
            params={"model": "llama-2-7b"},
            json= {"prompt": prompt}
        )
        
        return response.content
    finally:
        response.close()
    
   
# TODO: GRPC example for talking to predictor  
@app.route('/torch/image/predict_grpc', defaults={'model_name': None}, methods=['POST'])
@app.route('/torch/image/predict_grpc/<model_name>', methods=['POST'])
def torch_predict_grc(model_name):
    
    # register the model
    body = request.files
    
    # check model status
    
    # send model prediction request
    
    return
