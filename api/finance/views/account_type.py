import json

from flask import abort, jsonify, request, Response
from flask.views import MethodView

import config

from finance import utils, db
from finance.forms.account_type import AccountTypeForm
from finance.models.account_type import AccountType
from finance.stats import STATS


class AccountTypeAPI(MethodView):
    """Account Type Views"""

    decorators = [
        utils.requires_auth,
        utils.crossdomain(
            origin='*',
            headers=config.HEADERS_ALLOWED
        ),
    ]

    def get(self, account_type_id):
        if account_type_id is None:
            with STATS.all_account_types.time():
                # return a list of account types
                res = [
                    at.jsonify() for at in AccountType.query.all()
                ]
                STATS.success += 1
                return Response(json.dumps(res), mimetype='application/json')
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
                db.session.add(acct_type)
                db.session.commit()
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
            db.session.delete(acct_type)
            db.session.commit()
            STATS.success += 1
            return jsonify({"message": "Successfully deleted Account Type"})

    def put(self, account_type_id):
        with STATS.update_account_type.time():
            # update a single account type
            acct_type = AccountType.query.get(account_type_id)
            if acct_type is None:
                STATS.notfound += 1
                return abort(404)
            form = AccountTypeForm(request.data,
                                   account_type_id=account_type_id)
            if form.validate():
                acct_type = AccountType.query.get(account_type_id)
                acct_type.name = form.name.data
                db.session.add(acct_type)
                db.session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully updated Account Type'
                })
            STATS.validation += 1
            resp = jsonify({'errors': form.errors})
            resp.status_code = 400
            return resp
