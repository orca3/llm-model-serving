from inference.app import app

# Use blueprint to convert this separate module to have its own routing. 
@app.route('/pytorch/local/inference/<model_name>')
def get_pytorch_serv(model_name):
    return "receive prediction request for pytorch model {}".format(model_name)

@app.route("/home3")
def home3():
    return "Hello, Flask333!"