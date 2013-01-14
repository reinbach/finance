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


test_cases = [
    TransactionViewTestCase
]