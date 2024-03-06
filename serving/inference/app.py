from . import create_app

app = create_app()

import inference.local

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/home")
def home2():
    return "Hello, Flask222!"