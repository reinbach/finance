import json

from flask import abort, jsonify, request, Response
from flask.views import MethodView
from werkzeug.datastructures import MultiDict

import config

from finance import utils, db
from finance.forms.transaction import TransactionForm, TransactionsImportForm
from finance.models.transaction import Transaction
from finance.stats import STATS
from finance.trx_import import TransactionsImport


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
                    form.debit.account,
                    form.credit.account,
                    form.amount.data,
                    form.summary.data,
                    form.date.data,
                    form.description.data
                )
                db.session.add(trx)
                db.session.commit()
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
            db.session.delete(trx)
            db.session.commit()
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
                db.session.add(trx)
                db.session.commit()
                STATS.success += 1
                return jsonify({
                    'message': 'Successfully updated Transaction'
                })
            STATS.validation += 1
            resp = jsonify({'errors': form.errors})
            resp.status_code = 400
            return resp


@utils.requires_auth
@utils.crossdomain(origin='*', headers=config.HEADERS_ALLOWED)
def transactions_import():
    """Import transactions"""
    with STATS.upload_transactions.time():
        form = TransactionsImportForm(MultiDict(request.data))
        if form.validate():
            importer = TransactionsImport(form.account.data,
                                          form.transactions_file.data)
            transaction_list = []
            for trx in importer.parse_file():
                transaction_list.append(trx.jsonify())
            STATS.success += 1
            return jsonify(trx)
        resp = jsonify(form.errors)
        resp.status_code = 400
        return resp
