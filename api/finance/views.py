from flask import abort, jsonify, request
from flask.views import MethodView

import utils

from finance import db_session
from forms import AccountForm
from models import Account

class AccountAPI(MethodView):
    """Account Views"""

    decorators = [utils.requires_auth]

    def get(self, account_id):
        if account_id is None:
            # return a list of accounts
            res = {'accounts': [acct.jsonify() for acct in Account.query.all()]}
            return jsonify(res)
        else:
            # expose a single account
            acct = Account.query.get(account_id)
            if acct is None:
                return abort(404)
            return jsonify(acct.jsonify())

    def post(self):
        # create a new account
        form = AccountForm(request.form)
        if form.validate():
            acct = Account(
                form.name.data,
                form.account_type.data,
                form.description.data
            )
            db_session.add(acct)
            db_session.commit()
            return jsonify({
                'message': 'Successfully added Account',
                'account_id': acct.account_id
            })
        return jsonify({"errors": form.errors})

    def delete(self, account_id):
        # delete a single account
        acct = Account.query.get(account_id)
        if acct is None:
            return abort(404)
        db_session.delete(acct)
        db_session.commit()
        return jsonify({"message": "Successfully deleted account"})

    def put(self, account_id):
        # update a single account
        form = AccountForm(request.form)
        if form.validate():
            acct = Account.query.get(account_id)
            acct.name = form.name.data
            acct.account_type = form.account_type.data
            acct.description = form.description.data
            db_session.add(acct)
            db_session.commit()
            return jsonify({
                'message': 'Successfully updated Account'
            })
        return jsonify({'errors': form.errors})

