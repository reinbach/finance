from flask import abort, jsonify, request
from flask.views import MethodView

from finance import db_session, utils
from finance.forms import AccountForm
from finance.models import Account
from finance.stats import STATS

class AccountAPI(MethodView):
    """Account Views"""

    decorators = [utils.requires_auth]

    def get(self, account_id):
        if account_id is None:
            with STATS.all_accounts.time():
                # return a list of accounts
                res = {'accounts': [acct.jsonify() for acct in Account.query.all()]}
                STATS.success += 1
                return jsonify(res)
        else:
            with STATS.get_account.time():
                # expose a single account
                acct = Account.query.get(account_id)
                if acct is None:
                    STATS.notfound += 1
                    return abort(404)
                STATS.success += 1
                return jsonify(acct.jsonify())

    def post(self):
        with STATS.add_account.time():
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
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully added Account',
                    'account_id': acct.account_id
                })
            STATS.validation += 1
            return jsonify({"errors": form.errors})

    def delete(self, account_id):
        with STATS.delete_account.time():
            # delete a single account
            acct = Account.query.get(account_id)
            if acct is None:
                STATS.notfound += 1
                return abort(404)
            db_session.delete(acct)
            db_session.commit()
            STATS.success += 1
            return jsonify({"message": "Successfully deleted account"})

    def put(self, account_id):
        with STATS.update_account.time():
            # update a single account
            form = AccountForm(request.form)
            if form.validate():
                acct = Account.query.get(account_id)
                acct.name = form.name.data
                acct.account_type = form.account_type.data
                acct.description = form.description.data
                db_session.add(acct)
                db_session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully updated Account'
                })
            STATS.validation += 1
            return jsonify({'errors': form.errors})
