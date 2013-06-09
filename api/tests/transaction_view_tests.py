import datetime
import json

from finance.models import Account, AccountType, Transaction, db_session
from view_tests import BaseViewTestCase

class TransactionViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(TransactionViewTestCase, self).setUp()
        self.account_type = AccountType('Income')
        db_session.add(self.account_type)
        db_session.commit()
        self.account1 = Account('TRX_Salary', self.account_type.account_type_id, "Show me the money")
        self.account2 = Account('TRX_Checking', self.account_type.account_type_id, "Mine mine mine")
        db_session.add(self.account1)
        db_session.add(self.account2)
        db_session.commit()
        self.transaction = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10000,
            'Employer',
            datetime.date.today(),
            'January'
        )
        db_session.add(self.transaction)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.transaction)
        db_session.delete(self.account1)
        db_session.delete(self.account2)
        db_session.delete(self.account_type)
        super(TransactionViewTestCase, self).tearDown()

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/transactions")
        self.assertEqual(401, rv.status_code)

    def test_view_all(self):
        """Test viewing all transactions"""
        rv = self.open_with_auth(
            "/transactions",
            'GET',
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        trx = self.transaction.jsonify()
        self.assertIn(trx, data)

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
        date = datetime.date.today().strftime("%Y-%m-%d")
        description = 'Getting things done'
        debit_json = self.account1.jsonify()
        credit_json = self.account2.jsonify()
        rv = self.open_with_auth(
            "/transactions",
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
        # need to update account balances with this trx
        debit_json['balance'] += amount;
        credit_json['balance'] -= amount;
        self.assertEqual(debit_json, trx_get.get('debit'))
        self.assertEqual(debit_json.get('account_id'), trx_get.get('account_debit_id'))
        self.assertEqual(credit_json, trx_get.get('credit'))
        self.assertEqual(credit_json.get('account_id'), trx_get.get('account_credit_id'))
        self.assertEqual(summary, trx_get.get('summary'))
        self.assertEqual(amount, trx_get.get('amount'))
        self.assertEqual(date, trx_get.get('date'))
        self.assertEqual(description, trx_get.get('description'))
        self.assertEqual(trx.get('transaction_id'), trx_get.get('transaction_id'))

    def test_view_add_locale_date(self):
        """Test adding a transaction using a locale date value"""
        summary = 'Supplies'
        amount = 200.00
        date = '2013-01-15T05:00:00.000Z'
        description = 'Getting things done'
        debit_json = self.account1.jsonify()
        credit_json = self.account2.jsonify()
        rv = self.open_with_auth(
            "/transactions",
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
        # need to update account balances with this trx
        debit_json['balance'] += amount;
        credit_json['balance'] -= amount;
        self.assertEqual(debit_json, trx_get.get('debit'))
        self.assertEqual(debit_json.get('account_id'), trx_get.get('account_debit_id'))
        self.assertEqual(credit_json, trx_get.get('credit'))
        self.assertEqual(credit_json.get('account_id'), trx_get.get('account_credit_id'))
        self.assertEqual(summary, trx_get.get('summary'))
        self.assertEqual(amount, trx_get.get('amount'))
        self.assertEqual(date[:10], trx_get.get('date'))
        self.assertEqual(description, trx_get.get('description'))
        self.assertEqual(trx.get('transaction_id'), trx_get.get('transaction_id'))

    def test_view_add_fail(self):
        """Test adding an invalid transaction"""
        summary = 'Supplies'
        amount = -100.00
        date = datetime.date.today().strftime("%Y-%m-%d")
        description = 'Getting things done'
        debit_json = self.account1.jsonify()
        credit_json = self.account2.jsonify()
        rv = self.open_with_auth(
            "/transactions",
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
        self.assertEqual(400, rv.status_code)
        self.assertIn('errors', rv.data)

    def test_view_account_transactions(self):
        """Test viewing transactions for an account"""
        rv = self.open_with_auth(
            '/accounts/transactions/%s' % self.account1.account_id,
            'GET',
            self.username,
            self.password
        )
        acct_trx_list = json.loads(rv.data)
        self.assertEqual(len(acct_trx_list), 1)
        self.assertIn(self.account1.transactions()[0].jsonify(), acct_trx_list)

    def test_view_delete(self):
        """Test deleting transaction"""
        transaction1 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            100.00,
            'Bonus',
            datetime.date.today().strftime("%Y-%m-%d")
        )
        db_session.add(transaction1)
        db_session.commit()
        rv = self.open_with_auth(
            "/transactions/%s" % transaction1.transaction_id,
            "DELETE",
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)

        # attempt to get the transaction
        rv = self.open_with_auth(
            "/transactions/%s" % transaction1.transaction_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

    def test_view_delete_fail(self):
        """Test deleting a non existant transaction"""
        rv = self.open_with_auth(
            "/transactions/999",
            "DELETE",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

    def test_view_update(self):
        """Test updating an transaction"""
        description = 'Something witty here'
        transaction_id = self.transaction.transaction_id
        rv = self.open_with_auth(
            "/transactions/%s" % transaction_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                debit=self.transaction.account_debit_id,
                credit=self.transaction.account_credit_id,
                amount=self.transaction.amount,
                summary=self.transaction.summary,
                date=self.transaction.date.strftime("%Y-%m-%d"),
                description=description,
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

        rv = self.open_with_auth(
            "/transactions/%s" % transaction_id,
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        trx_get = json.loads(rv.data)
        self.assertEqual(description, trx_get.get('description'))

    def test_view_update_nochange(self):
        """Test updating an transaction with same values"""
        transaction_id = self.transaction.transaction_id
        rv = self.open_with_auth(
            "/transactions/%s" % transaction_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                debit=self.transaction.account_debit_id,
                credit=self.transaction.account_credit_id,
                amount=self.transaction.amount,
                summary=self.transaction.summary,
                date=self.transaction.date.strftime("%Y-%m-%d"),
                description=self.transaction.description,
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

    def test_view_update_fail_invalid_id(self):
        """Test updating an transaction with invalid id"""
        transaction_id = '999'
        rv = self.open_with_auth(
            "/transactions/%s" % transaction_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                debit=self.transaction.account_debit_id,
                credit=self.transaction.account_credit_id,
                amount=self.transaction.amount,
                summary=self.transaction.summary,
                date=self.transaction.date.strftime("%Y-%m-%d"),
                description=self.transaction.description,
            )
        )
        self.assertEqual(404, rv.status_code)


test_cases = [
    TransactionViewTestCase
]