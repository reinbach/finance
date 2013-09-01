import datetime
import json

from finance.models.account import Account, db
from finance.models.account_type import AccountType
from finance.models.transaction import Transaction


class TestTransactionModel():

    def setup_method(self, method):
        self.account_type = AccountType('Income')
        db.session.add(self.account_type)
        db.session.commit()
        self.account1 = Account("Test1", self.account_type.account_type_id)
        self.account2 = Account("Test2", self.account_type.account_type_id)
        db.session.add(self.account1)
        db.session.add(self.account2)
        db.session.commit()

    def teardown_method(self, method):
        db.session.delete(self.account_type)
        db.session.delete(self.account1)
        db.session.delete(self.account2)
        db.session.commit()
        db.session.remove()

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        t = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            1,
            "ACME, Inc.",
            datetime.date.today(),
            "January's Salary"
        )
        assert bool(t) is True

    def test_transaction_add(self):
        """Test adding a transaction normaly"""
        t = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            1,
            "ACME, Inc.",
            datetime.date.today(),
            "January's Salary"
        )

        db.session.add(t)
        db.session.commit()

        t2 = Transaction.query.filter(Transaction.amount == t.amount).first()
        assert t2.account_debit_id == t.account_debit_id
        assert t2.account_credit_id == t.account_credit_id
        assert t2.amount == t.amount
        assert t2.summary == t.summary
        assert t2.description == t.description
        assert t2.date == t.date
        assert bool(t2.transaction_id) is True

    def test_account_balance(self):
        """Test that balance on account calculates correctly"""
        t1 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "January's Salary'"
        )

        db.session.add(t1)

        t2 = Transaction(
            self.account2.account_id,
            self.account1.account_id,
            5,
            'IRS',
            datetime.date.today(),
            "Taxes for January'"
        )

        db.session.add(t2)
        db.session.commit()

        assert self.account1.get_balance() == t1.amount - t2.amount
        assert self.account2.get_balance() == t2.amount - t1.amount

    def test_account_balance_onesided(self):
        """Test that balance on account calculates correctly"""
        t1 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "January's Salary'"
        )

        db.session.add(t1)

        t2 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "February's Salary'"
        )

        db.session.add(t2)
        db.session.commit()

        assert self.account1.get_balance() == t1.amount + t2.amount
        assert self.account2.get_balance() == -t1.amount - t2.amount

    def test_account_transactions(self):
        """Test getting a list of transactions for an account"""
        acct1_trx_count = len(self.account1.transactions())
        acct2_trx_count = len(self.account2.transactions())
        t1 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "January's Salary'"
        )

        db.session.add(t1)

        t2 = Transaction(
            self.account2.account_id,
            self.account1.account_id,
            5,
            'IRS',
            datetime.date.today(),
            "Taxes for January'"
        )

        db.session.add(t2)
        db.session.commit()

        assert t1 in self.account1.transactions()
        assert t2 in self.account1.transactions()
        assert acct1_trx_count + 2 == len(self.account1.transactions())
        assert t1 in self.account2.transactions()
        assert t2 in self.account2.transactions()
        assert acct2_trx_count + 2 == len(self.account2.transactions())

    def test_transaction_jsonify(self):
        """Test the jsonify method"""
        t = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "January's Salary'"
        )
        assert dict == type(t.jsonify())
        assert bool(json.dumps(t.jsonify())) is True

        db.session.add(t)
        db.session.commit()

        t_json = t.jsonify()
        assert dict == type(t_json)
        assert bool(json.dumps(t_json)) is True
        assert self.account1.jsonify() == t_json.get('debit')
        assert self.account2.jsonify() == t_json.get('credit')
