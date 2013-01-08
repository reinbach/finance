import json

from flask import Flask

import config, utils

from finance.database import get_db_session
from finance.views import UserAPI

app = Flask(__name__)
app.config.from_object(config)

db_session = get_db_session()

utils.register_api(app, UserAPI, 'user_api', '/users/', pk='user_id')

@app.route("/")
def version():
    return json.dumps({"version": "0.1"})

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()