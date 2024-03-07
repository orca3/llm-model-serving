from inference.app import app
from flask import jsonify, request
from pytorch.image_classification import get_prediction

@app.route("/home3")
def home3():
    return "Hello, Flask333!"

@app.route('/image/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # we will get the file from the request
        file = request.files['img']
        # convert that to bytes
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_id': class_id, 'class_name': class_name})