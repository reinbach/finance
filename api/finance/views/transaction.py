from flask import abort, jsonify, request
from flask.views import MethodView

from finance import db_session, utils
from finance.forms import AccountForm
from finance.models import Transaction
from finance.stats import STATS

class TransactionAPI(MethodView):
    """Transaction Views"""

    decorators = [utils.requires_auth]

    def get(self, transaction_id):
        if transaction_id is None:
            # return a list of transactions
            with STATS.all_transactions.time():
                # return a list of accounts
                res = {'transactions': [trx.jsonify() for trx in Transaction.query.all()]}
                STATS.success += 1
                return jsonify(res)
        else:
            # expose transaction
            with STATS.get_transaction.time():
                # expose a single account
                trx = Transaction.query.get(transaction_id)
                if trx is None:
                    STATS.notfound += 1
                    return abort(404)
                STATS.success += 1
                return jsonify(trx.jsonify())

    def post(self):
        # add transaction
        pass

    def delete(self, transaction_id):
        # delete Transaction
        pass

    def put(self, Transaction_id):
        # update transaction
        pass