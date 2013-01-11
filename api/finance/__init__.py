from flask import Flask, jsonify

import config, utils

from finance.database import get_db_session

app = Flask(__name__)
app.config.from_object(config)

db_session = get_db_session()

from finance.views import AccountAPI
utils.register_api(app, AccountAPI, 'account_api', '/accounts/', pk='account_id')

@app.route("/")
def version():
    return jsonify({"version": "0.1"})

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()