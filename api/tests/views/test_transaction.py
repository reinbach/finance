import datetime
import json

from finance import app, db
from finance.models.account import Account
from finance.models.account_type import AccountType
from finance.models.transaction import Transaction
from tests.fixtures import setup_user, delete_user
from tests.views.test_base import BaseViewTestCase


class TestTransactionView(BaseViewTestCase):

    def setup_method(self, method):
        self.user, self.username, self.password = setup_user()
        self.app = app.test_client()
        self.account_type = AccountType('Income')
        db.session.add(self.account_type)
        db.session.commit()
        self.account1 = Account('TRX_Salary',
                                self.account_type.account_type_id,
                                "Show me the money")
        self.account2 = Account('TRX_Checking',
                                self.account_type.account_type_id,
                                "Mine mine mine")
        db.session.add(self.account1)
        db.session.add(self.account2)
        db.session.commit()
        self.transaction = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10000,
            'Employer',
            datetime.date.today(),
            'January'
        )
        db.session.add(self.transaction)
        db.session.commit()

    def teardown_method(self, method):
        delete_user(self.user)
        db.session.delete(self.transaction)
        db.session.delete(self.account1)
        db.session.delete(self.account2)
        db.session.delete(self.account_type)

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/transactions")
        assert 401 == rv.status_code

    def test_view_all(self):
        """Test viewing all transactions"""
        rv = self.open_with_auth(
            "/transactions",
            'GET',
            self.username,
            self.password
        )
        assert 200 == rv.status_code
        data = json.loads(rv.data)
        trx = self.transaction.jsonify()
        assert trx in data

    def test_view_transaction(self):
        """Test viewing a single transaction"""
        rv = self.open_with_auth(
            "/transactions/%s" % self.transaction.transaction_id,
            "GET",
            self.username,
            self.password
        )
        assert 200 == rv.status_code
        assert self.transaction.jsonify() == json.loads(rv.data)

    def test_view_transaction_404(self):
        """Test viewing a non-existant transaction"""
        rv = self.open_with_auth(
            "/transaction/999",
            "GET",
            self.username,
            self.password
        )
        assert 404 == rv.status_code
        assert "404 Not Found" in rv.data

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
        assert 200 == rv.status_code
        assert 'Success' in rv.data

        trx = json.loads(rv.data)
        rv = self.open_with_auth(
            "/transactions/%s" % trx.get('transaction_id'),
            "GET",
            self.username,
            self.password,
        )

        assert 200 == rv.status_code
        trx_get = json.loads(rv.data)
        # need to update account balances with this trx
        debit_json['balance'] += amount
        credit_json['balance'] -= amount
        assert debit_json == trx_get.get('debit')
        assert debit_json.get('account_id') == trx_get.get('account_debit_id')
        assert credit_json == trx_get.get('credit')
        assert credit_json.get('account_id') == trx_get.get(
            'account_credit_id'
        )
        assert summary == trx_get.get('summary')
        assert amount == trx_get.get('amount')
        assert date == trx_get.get('date')
        assert description == trx_get.get('description')
        assert trx.get('transaction_id') == trx_get.get('transaction_id')

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
        assert 200 == rv.status_code
        assert 'Success' in rv.data

        trx = json.loads(rv.data)
        rv = self.open_with_auth(
            "/transactions/%s" % trx.get('transaction_id'),
            "GET",
            self.username,
            self.password,
        )

        assert 200 == rv.status_code
        trx_get = json.loads(rv.data)
        # need to update account balances with this trx
        debit_json['balance'] += amount
        credit_json['balance'] -= amount
        assert debit_json == trx_get.get('debit')
        assert debit_json.get('account_id') == trx_get.get('account_debit_id')
        assert credit_json == trx_get.get('credit')
        assert credit_json.get('account_id') == trx_get.get(
            'account_credit_id'
        )
        assert summary == trx_get.get('summary')
        assert amount == trx_get.get('amount')
        assert date[:10] == trx_get.get('date')
        assert description == trx_get.get('description')
        assert trx.get('transaction_id') == trx_get.get('transaction_id')

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
        assert 400 == rv.status_code
        assert 'errors' in rv.data

    def test_view_account_transactions(self):
        """Test viewing transactions for an account"""
        rv = self.open_with_auth(
            '/accounts/transactions/%s' % self.account1.account_id,
            'GET',
            self.username,
            self.password
        )
        acct_trx_list = json.loads(rv.data)
        assert len(acct_trx_list) == 1
        assert self.account1.transactions()[0].jsonify() in acct_trx_list

    def test_view_delete(self):
        """Test deleting transaction"""
        transaction1 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            100.00,
            'Bonus',
            datetime.date.today().strftime("%Y-%m-%d")
        )
        db.session.add(transaction1)
        db.session.commit()
        rv = self.open_with_auth(
            "/transactions/%s" % transaction1.transaction_id,
            "DELETE",
            self.username,
            self.password
        )
        assert 200 == rv.status_code

        # attempt to get the transaction
        rv = self.open_with_auth(
            "/transactions/%s" % transaction1.transaction_id,
            "GET",
            self.username,
            self.password
        )
        assert 404 == rv.status_code

    def test_view_delete_fail(self):
        """Test deleting a non existant transaction"""
        rv = self.open_with_auth(
            "/transactions/999",
            "DELETE",
            self.username,
            self.password
        )
        assert 404 == rv.status_code

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
        assert 200 == rv.status_code
        assert 'Success' in rv.data

        rv = self.open_with_auth(
            "/transactions/%s" % transaction_id,
            "GET",
            self.username,
            self.password,
        )

        assert 200 == rv.status_code
        trx_get = json.loads(rv.data)
        assert description == trx_get.get('description')

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
        assert 200 == rv.status_code
        assert 'Success' in rv.data

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
        assert 404 == rv.status_code
