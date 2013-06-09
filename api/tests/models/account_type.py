import json
import unittest

from sqlalchemy.exc import IntegrityError

from finance.models.account_type import AccountType, db_session

class AccountTypeModelTestCase(unittest.TestCase):

    def tearDown(self):
        db_session.remove()

    def test_account_type_repr(self):
        at = AccountType('Expenses')
        self.assertTrue(at)

    def test_account_type_add(self):
        """Test adding an account type normally"""
        at = AccountType('Random')
        self.assertEqual(at.name, 'Random')

        db_session.add(at)
        db_session.commit()

        at2 = AccountType.query.filter(AccountType.name == at.name).first()
        self.assertEqual(at2.name, at.name)
        self.assertTrue(at2.account_type_id)

    def test_account_type_name_unique(self):
        """Test that account type name uniqueness is maintained"""
        at = AccountType('Interest Income')
        db_session.add(at)
        db_session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "account_types_name_key"'
        ):
            at2 = AccountType("Interest Income")
            db_session.add(at2)
            db_session.commit()

    def test_account_type_jsonify(self):
        """Test the jsonify method"""
        at = AccountType('Income')
        self.assertEqual(dict, type(at.jsonify()))
        self.assertTrue(json.dumps(at.jsonify()))

test_cases = [
    AccountTypeModelTestCase,
]