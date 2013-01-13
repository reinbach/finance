import datetime
import json
import unittest

from finance.models import Account, Transaction, db_session

class TransactionModelTestCase(unittest.TestCase):

    def setUp(self):
        self.account1 = Account("Test1", "Income")
        self.account2 = Account("Test2", "Expense")
        db_session.add(self.account1)
        db_session.add(self.account2)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.account1)
        db_session.delete(self.account2)
        db_session.commit()
        db_session.remove()

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        t = Transaction(
            self.account1,
            self.account2,
            1,
            "ACME, Inc.",
            "January's Salary",
            datetime.date.today()
        )
        self.assertTrue(t)

    def test_transaction_add(self):
        """Test adding a transaction normaly"""
        t = Transaction(
            self.account1,
            self.account2,
            1,
            "ACME, Inc.",
            "January's Salary",
            datetime.date.today()
        )

        db_session.add(t)
        db_session.commit()

        t2 = Transaction.query.filter(Transaction.amount == t.amount).first()
        self.assertEqual(t2.account_debit_id, t.account_debit_id)
        self.assertEqual(t2.account_credit_id, t.account_credit_id)
        self.assertEqual(t2.amount, t.amount)
        self.assertEqual(t2.summary, t.summary)
        self.assertEqual(t2.description, t.description)
        self.assertEqual(t2.date, t.date)
        self.assertTrue(t2.transaction_id)

    def test_account_balance(self):
        """Test that balance on account calculates correctly"""
        t1 = Transaction(
            self.account1,
            self.account2,
            10,
            'ACME, Inc.',
            "January's Salary'",
            datetime.date.today()
        )

        db_session.add(t1)

        t2 = Transaction(
            self.account2,
            self.account1,
            5,
            'IRS',
            "Taxes for January'",
            datetime.date.today()
        )

        db_session.add(t2)
        db_session.commit()

        self.assertEqual(self.account1.get_balance(), t1.amount - t2.amount)
        self.assertEqual(self.account2.get_balance(), t2.amount - t1.amount)

    def test_account_balance_onesided(self):
        """Test that balance on account calculates correctly"""
        t1 = Transaction(
            self.account1,
            self.account2,
            10,
            'ACME, Inc.',
            "January's Salary'",
            datetime.date.today()
        )

        db_session.add(t1)

        t2 = Transaction(
            self.account1,
            self.account2,
            10,
            'ACME, Inc.',
            "February's Salary'",
            datetime.date.today()
        )

        db_session.add(t2)
        db_session.commit()

        self.assertEqual(self.account1.get_balance(), t1.amount + t2.amount)
        self.assertEqual(self.account2.get_balance(), -t1.amount - t2.amount)

    def test_transaction_jsonify(self):
        """Test the jsonify method"""
        t = Transaction(
            self.account1,
            self.account2,
            10,
            'ACME, Inc.',
            "January's Salary'",
            datetime.date.today()
        )
        self.assertEqual(dict, type(t.jsonify()))
        self.assertTrue(json.dumps(t.jsonify()))

test_cases = [
    TransactionModelTestCase
]