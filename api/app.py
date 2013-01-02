import json

from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def version():
    return json.dumps({"version": "0.1"})

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()