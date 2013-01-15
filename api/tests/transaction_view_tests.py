import datetime
import json

from finance.models import Account, Transaction, db_session
from view_tests import BaseViewTestCase

class TransactionViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(TransactionViewTestCase, self).setUp()
        self.account1 = Account('TRX_Salary', 'Income', "Show me the money")
        self.account2 = Account('TRX_Checking', 'Assets', "Mine mine mine")
        self.transaction = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10000,
            'Employer',
            datetime.date.today(),
            'January'
        )
        db_session.add(self.account1)
        db_session.add(self.account2)
        db_session.add(self.transaction)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.account1)
        db_session.delete(self.account2)
        db_session.delete(self.transaction)
        super(TransactionViewTestCase, self).tearDown()

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/transactions/")
        self.assertEqual(401, rv.status_code)

    def test_view_all(self):
        """Test viewing all transactions"""
        rv = self.open_with_auth(
            "/transactions/",
            'GET',
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        trx = self.transaction.jsonify()
        self.assertIn(trx, data['transactions'])

    def test_view_transaction(self):
        """Test viewing a single transaction"""
        rv = self.open_with_auth(
            "/transactions/%s" % self.transaction.transaction_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(self.transaction.jsonify(), json.loads(rv.data))

    def test_view_transaction_404(self):
        """Test viewing a non-existant transaction"""
        rv = self.open_with_auth(
            "/transaction/999",
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)
        self.assertIn("404 Not Found", rv.data)

    def test_view_add(self):
        """Test adding a transaction"""
        summary = 'Supplies'
        amount = 100.00
        date = datetime.date.today()
        description = 'Getting things done'
        debit_json = self.account1.jsonify()
        credit_json = self.account2.jsonify()
        rv = self.open_with_auth(
            "/transactions/",
            "POST",
            self.username,
            self.password,
            data=dict(
                debit=debit_json.get('account_id'),
                credit=credit_json.get('account_id'),
                amount=amount,
                summary=summary,
                date=date,
                description=description
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)


        trx = json.loads(rv.data)
        rv = self.open_with_auth(
            "/transactions/%s" % trx.get('transaction_id'),
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        trx_get = json.loads(rv.data)
        self.assertEqual(debit_json, trx_get.get('debit'))
        self.assertEqual(debit_json.get('account_id'), trx_get.get('account_debit_id'))
        self.assertEqual(credit_json, trx_get.get('credit'))
        self.assertEqual(credit_json.get('account_id'), trx_get.get('account_credit_id'))
        self.assertEqual(summary, trx_get.get('summary'))
        self.assertEqual(amount, trx_get.get('amount'))
        self.assertEqual(date.strftime("%Y-%m-%d"), trx_get.get('date'))
        self.assertEqual(description, trx_get.get('description'))
        self.assertEqual(trx.get('transaction_id'), trx_get.get('transaction_id'))


test_cases = [
    TransactionViewTestCase
]