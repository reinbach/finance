import json

from flask import Flask

import config, utils

app = Flask(__name__)
app.config.from_object(config)

from finance.views import UserAPI

utils.register_api(app, UserAPI, 'user_api', '/users/', pk='user_id')

@app.route("/")
def version():
    return json.dumps({"version": "0.1"})

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()