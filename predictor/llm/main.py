from llama_cpp import Llama
import json, os
from flask import Flask, request, jsonify

app = Flask(__name__)

model_dir = os.getenv("MODEL_DIR", "../../models/llama")
host_ip = os.getenv("HOST_IP", "127.0.0.1")
host_port = os.getenv("HOST_PORT", "5000")
llama_model = Llama(model_path="{0}/llama-2-7b.Q2_K.gguf".format(model_dir))

@app.route("/stream", methods=['POST'])
def stream():
    """
    Summary:
        model streaming api on using llma-2-7b model, return the token as soon as the model produces it. 
    
        Use following curl command to test this api
        curl -N -X POST http://127.0.0.1:5000/stream \
            -H "Content-Type: application/json" \
            -d "{\"prompt\":\"What is the capital of USA?\"}" 
            
    Returns:
        _type_: stream: a serial of tokens (string)    
    """
    data = request.get_json()
    prompt = data['prompt']
    
    def generate():
        
        if not prompt:
            yield ''
        
        output = llama_model(
            prompt, # Prompt
            max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
            stop=[], # Stop generating just before the model would generate a new question
            echo=False, # Echo the prompt back in the output
            stream = True
        ) # Generate a completion, can also call create_completion
        
        for item in output:
            print(item['choices'][0]['text'], end = '')
            if item['choices'] and item['choices'][0] and item['choices'][0]['text']:
                yield json.dumps(item['choices'][0])
                # yield item['choices'][0]['text']

    return app.response_class(generate(), content_type='text/event-stream')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Summary:
        LLM prediction api, return the full generated output from model all at once. 
    
        Use following curl command to test this api
        curl -X POST 'http://localhost:5000/predict?model=llama-2-7b' \
            -H 'Content-Type: application/json' \
            -d "{\"prompt\":\"What is the capital of USA?\"}"
            
    Returns:
        _type_: string    
    """
    
    # Extract the 'model' parameter from the query string
    model_name = request.args.get('model', None)
    if not model_name:
        return jsonify({"error": "Missing model parameter"}), 400
    
    model = llama_model
    
    # [Future Work]
    # if model_name != "llama-2-7b":
    #     model = # load model and cache... 
    
    # Parse the JSON payload
    data = request.get_json()
    prompt = data['prompt']

    # Check if the payload is empty or not JSON
    if not data or not prompt:
        return jsonify({"error": "Missing or invalid JSON payload"}), 400

    output = model(
        prompt, # Prompt
        max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
        stop=[], # Stop generating just before the model would generate a new question
        echo=False # Echo the prompt back in the output
    )

    return output, 200

app.run(host=host_ip, port=int(host_port), debug=True)

