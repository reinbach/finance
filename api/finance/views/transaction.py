import json

from flask import abort, jsonify, request, Response
from flask.views import MethodView

import config

from finance import app, utils
from finance.forms.transaction import TransactionForm
from finance.models.transaction import Transaction
from finance.stats import STATS


class TransactionAPI(MethodView):
    """Transaction Views"""

    decorators = [
        utils.requires_auth,
        utils.crossdomain(
            origin='*',
            headers=config.HEADERS_ALLOWED
        ),
    ]

    def get(self, transaction_id):
        if transaction_id is None:
            # return a list of transactions
            with STATS.all_transactions.time():
                # return a list of accounts
                res = [trx.jsonify() for trx in Transaction.query.all()]
                STATS.success += 1
                return Response(json.dumps(res), mimetype='application/json')
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
        with STATS.add_transaction.time():
            # create a new trasnsaction
            form = TransactionForm(request.data)
            if form.validate():
                trx = Transaction(
                    form.debit.data,
                    form.credit.data,
                    form.amount.data,
                    form.summary.data,
                    form.date.data,
                    form.description.data
                )
                app.db.session.add(trx)
                app.db.session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully added Transaction',
                    'transaction_id': trx.transaction_id
                })
            STATS.validation += 1
            resp = jsonify({"errors": form.errors})
            resp.status_code = 400
            return resp

    def delete(self, transaction_id):
        with STATS.delete_transaction.time():
            # delete a single transaction
            trx = Transaction.query.get(transaction_id)
            if trx is None:
                STATS.notfound += 1
                return abort(404)
            app.db.session.delete(trx)
            app.db.session.commit()
            STATS.success += 1
            return jsonify({"message": "Successfully deleted transaction"})

    def put(self, transaction_id):
        with STATS.update_transaction.time():
            # update a single transaction
            trx = Transaction.query.get(transaction_id)
            if trx is None:
                STATS.notfound += 1
                return abort(404)
            form = TransactionForm(request.data)
            if form.validate():
                trx = Transaction.query.get(transaction_id)
                trx.account_debit_id = form.debit.data
                trx.account_credit_id = form.credit.data
                trx.amount = form.amount.data
                trx.summary_id = form.summary.data
                trx.date = form.date.data
                trx.description = form.description.data
                app.db.session.add(trx)
                app.db.session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully updated Transaction'
                })
            STATS.validation += 1
            resp = jsonify({'errors': form.errors})
            resp.status_code = 400
            return resp
