import datetime
import unittest

from finance.models import Account, Transaction, db_session

class TransactionModelTestCase(unittest.TestCase):

    def setUp(self):
        self.account1 = Account("Test1", "Income")
        self.account2 = Account("Test2", "Expense")

    def tearDown(self):
        db_session.remove()

    def test_transaction_add(self):
        """Test adding a transaction normaly"""
        t = Transaction(self.account1, self.account2, 1, "ACME, Inc.", "January's Salary", datetime.date.today())

        db_session.add(t)
        db_session.commit()

        t2 = Transaction.query.filter(Transaction.amount == t.amount).first()
        self.assertEqual(t2.account_debit, t.account_debit)
        self.assertEqual(t2.account_credit, t.account_credit)
        self.assertEqual(t2.amount, t.amount)
        self.assertEqual(t2.summary, t.summary)
        self.assertEqual(t2.description, t.description)
        self.assertEqual(t2.date, t.date)
        self.assertTrue(t2.transaction_id)


test_cases = [
    TransactionModelTestCase
]