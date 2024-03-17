from . import create_app

app = create_app()

import inference.local
import inference.proxy

@app.route("/")
def default():
    return "Hello, Inference Service (Flask)!"
