from flask import Flask, jsonify, request

import config, utils

from finance.database import get_db_session
from finance.forms import UserForm
from finance.utils import Auth

app = Flask(__name__)
app.config.from_object(config)
app.auth = Auth()

db_session = get_db_session()

from finance.views.account_type import AccountTypeAPI
utils.register_api(app, AccountTypeAPI, 'account_type_api', '/account/types', pk='account_type_id')

from finance.views.account import AccountAPI, transactions
utils.register_api(app, AccountAPI, 'account_api', '/accounts', pk='account_id')
app.add_url_rule(
    '/accounts/transactions/<int:account_id>',
    view_func=transactions,
    methods=['GET',]
)

from finance.views.transaction import TransactionAPI
utils.register_api(app, TransactionAPI, 'transaction_api', '/transactions', pk='transaction_id')

from finance.models.mapper import set_model_mapping
set_model_mapping()

@app.route("/")
def version():
    return jsonify({"version": "0.1"})

@app.route("/login", methods=['POST'])
@utils.crossdomain(origin='*', headers=config.HEADERS_ALLOWED)
def login():
    """Log user in"""
    form = UserForm(request.data)
    if form.validate():
        if utils.check_auth(form.username.data, form.password.data):
            return jsonify({
                'auth_token': app.auth.set_token(),
                'message': 'Successfully logged in.'
            })
        else:
            resp = jsonify({'message': 'Invalid username/password.'})
            resp.status_code = 400
            return resp
    resp = jsonify(form.errors)
    resp.status_code = 400
    return resp

@app.route("/logout")
@utils.crossdomain(origin='*', headers=config.HEADERS_ALLOWED)
def logout():
    app.auth.remove_token(request.headers.get('AuthToken'))
    return jsonify({'message': 'Successfully logged out.'})

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()