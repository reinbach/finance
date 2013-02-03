from flask import abort, jsonify, request
from flask.views import MethodView

from finance import db_session, utils
from finance.forms import AccountTypeForm
from finance.models import AccountType
from finance.stats import STATS

class AccountTypeAPI(MethodView):
    """Account Type Views"""

    decorators = [
        utils.requires_auth,
        utils.crossdomain(
            origin='*',
            headers='origin, x-requested-with, content-type, accept, authtoken'
        ),
    ]

    def get(self, account_type_id):
        if account_type_id is None:
            with STATS.all_account_types.time():
                # return a list of account types
                res = {'account_types': [
                    acct_type.jsonify() for acct_type in AccountType.query.all()
                ]}
                STATS.success += 1
                return jsonify(res)
        else:
            with STATS.get_account_type.time():
                # expose a single account type
                acct_type = AccountType.query.get(account_type_id)
                if acct_type is None:
                    STATS.notfound += 1
                    return abort(404)
                STATS.success += 1
                return jsonify(acct_type.jsonify())

    def post(self):
        with STATS.add_account_type.time():
            # create a new account type
            form = AccountTypeForm(request.data)
            if form.validate():
                acct_type = AccountType(
                    form.name.data,
                )
                db_session.add(acct_type)
                db_session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully added Account Type',
                    'account_type_id': acct_type.account_type_id
                })
            STATS.validation += 1
            resp = jsonify({"errors": form.errors})
            resp.status_code = 400
            return resp

    def delete(self, account_type_id):
        with STATS.delete_account_type.time():
            # delete a single account type
            acct_type = AccountType.query.get(account_type_id)
            if acct_type is None:
                STATS.notfound += 1
                return abort(404)
            db_session.delete(acct_type)
            db_session.commit()
            STATS.success += 1
            return jsonify({"message": "Successfully deleted Account Type"})

    def put(self, account_type_id):
        with STATS.update_account_type.time():
            # update a single account type
            form = AccountTypeForm(request.data)
            if form.validate():
                acct_type = AccountType.query.get(account_type_id)
                acct_type.name = form.name.data
                db_session.add(acct_type)
                db_session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully updated Account Type'
                })
            STATS.validation += 1
            resp = jsonify({'errors': form.errors})
            resp.status_code = 400
            return resp
