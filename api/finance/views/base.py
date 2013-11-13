from flask import jsonify, request

from finance import app, config, utils
from finance.forms import UserForm
from finance.views.account import AccountAPI, transactions
from finance.views.account_type import AccountTypeAPI
from finance.views.transaction import TransactionAPI


utils.register_api(app, AccountTypeAPI, 'account_type_api', '/account/types',
                   pk='account_type_id')
utils.register_api(app, AccountAPI, 'account_api', '/accounts',
                   pk='account_id')
app.add_url_rule(
    '/accounts/transactions/<int:account_id>',
    view_func=transactions,
    methods=['GET', ]
)
utils.register_api(app, TransactionAPI, 'transaction_api', '/transactions',
                   pk='transaction_id')


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
