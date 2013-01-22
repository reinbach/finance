from flask import Flask, jsonify, request, session

import config, utils

from finance.database import get_db_session
from finance.forms import UserForm

app = Flask(__name__)
app.config.from_object(config)

db_session = get_db_session()

from finance.views.account import AccountAPI
utils.register_api(app, AccountAPI, 'account_api', '/accounts/', pk='account_id')

from finance.views.transaction import TransactionAPI
utils.register_api(app, TransactionAPI, 'transaction_api', '/transactions/', pk='transaction_id')

@app.route("/")
def version():
    return jsonify({"version": "0.1"})

@app.route("/login", methods=['POST'])
def login():
    """Log user in"""
    form = UserForm(request.form)
    if form.validate():
        if utils.check_auth(form.username.data, form.password.data):
            session['logged_in'] = True
            return jsonify({'message': 'Successfully logged in.'})
        else:
            resp = jsonify({'message': 'Invalid username/password.'})
            resp.status_code = 401
            return resp
    return jsonify(form.errors)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify({'message': 'Successfully logged out.'})

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()