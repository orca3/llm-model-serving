from . import create_app

app = create_app()

import inference.local

@app.route("/")
def default():
    return "Hello, Inference Service (Flask)!"
