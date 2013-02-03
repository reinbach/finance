import datetime
import json
import unittest

from finance.models import Account, AccountType, Transaction, db_session

class TransactionModelTestCase(unittest.TestCase):

    def setUp(self):
        self.account_type = AccountType('Income')
        db_session.add(self.account_type)
        db_session.commit()
        self.account1 = Account("Test1", self.account_type.account_type_id)
        self.account2 = Account("Test2", self.account_type.account_type_id)
        db_session.add(self.account1)
        db_session.add(self.account2)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.account_type)
        db_session.delete(self.account1)
        db_session.delete(self.account2)
        db_session.commit()
        db_session.remove()

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
        self.assertTrue(t)

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
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "January's Salary'"
        )

        db_session.add(t1)

        t2 = Transaction(
            self.account2.account_id,
            self.account1.account_id,
            5,
            'IRS',
            datetime.date.today(),
            "Taxes for January'"
        )

        db_session.add(t2)
        db_session.commit()

        self.assertEqual(self.account1.get_balance(), t1.amount - t2.amount)
        self.assertEqual(self.account2.get_balance(), t2.amount - t1.amount)

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

        db_session.add(t1)

        t2 = Transaction(
            self.account1.account_id,
            self.account2.account_id,
            10,
            'ACME, Inc.',
            datetime.date.today(),
            "February's Salary'"
        )

        db_session.add(t2)
        db_session.commit()

        self.assertEqual(self.account1.get_balance(), t1.amount + t2.amount)
        self.assertEqual(self.account2.get_balance(), -t1.amount - t2.amount)

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
        self.assertEqual(dict, type(t.jsonify()))
        self.assertTrue(json.dumps(t.jsonify()))

        db_session.add(t)
        db_session.commit()

        t_json = t.jsonify()
        self.assertEqual(dict, type(t_json))
        self.assertTrue(json.dumps(t_json))
        self.assertEqual(self.account1.jsonify(), t_json.get('debit'))
        self.assertEqual(self.account2.jsonify(), t_json.get('credit'))

test_cases = [
    TransactionModelTestCase
]