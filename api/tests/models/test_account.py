import json
import unittest

from sqlalchemy.exc import IntegrityError

from finance.models.account import Account, db_session
from finance.models.account_type import AccountType

class AccountModelTestCase(unittest.TestCase):

    def setUp(self):
        self.account_type = AccountType('Income')
        db_session.add(self.account_type)
        db_session.commit()

    def tearDown(self):
        db_session.rollback()
        db_session.delete(self.account_type)
        db_session.commit()
        db_session.remove()

    def test_account_repr(self):
        """Ensure __repr__ function works"""
        a = Account('Bonus', self.account_type.account_type_id, "Show me the money")
        self.assertEqual(repr(a), '<Account: Bonus [Income]>')

    def test_account_add(self):
        """Test adding an account normaly"""
        a = Account("Salary", self.account_type.account_type_id, "Show me the money")
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
        a = Account("Interest", self.account_type.account_type_id, "Compound it baby")
        db_session.add(a)
        db_session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "accounts_name_key"'
        ):
            a2 = Account("Interest", self.account_type.account_type_id, "No, don't charge me'")
            db_session.add(a2)
            db_session.commit()

    def test_account_jsonify(self):
        """Test the jsonify method"""
        a = Account("Interest", self.account_type.account_type_id, "Compound it baby")
        self.assertEqual(dict, type(a.jsonify()))
        self.assertTrue(json.dumps(a.jsonify()))

test_cases = [
    AccountModelTestCase,
]