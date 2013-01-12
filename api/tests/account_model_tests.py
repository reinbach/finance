import unittest

from sqlalchemy.exc import IntegrityError

from finance.models import Account, db_session

class AccountModelTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        db_session.remove()

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        a = Account('Salary', 'Income', "Show me the money")
        self.assertTrue(a)

    def test_account_add(self):
        """Test adding an account normaly"""
        a = Account("Salary", "Income", "Show me the money")
        self.assertEqual(a.name, "Salary")

        db_session.add(a)
        db_session.commit()

        a2 = Account.query.filter(Account.name == a.name).first()
        self.assertEqual(a2.name, a.name)
        self.assertEqual(a2.account_type, a.account_type)
        self.assertEqual(a2.description, a.description)
        self.assertTrue(a2.account_id)

    def test_account_name_unique(self):
        """Test that account name uniqueness is maintained"""
        a = Account("Interest", "Income", "Compound it baby")
        db_session.add(a)
        db_session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "accounts_name_key"'
        ):
            a2 = Account("Interest", "Expense", "No, don't charge me'")
            db_session.add(a2)
            db_session.commit()

test_cases = [
    AccountModelTestCase
]