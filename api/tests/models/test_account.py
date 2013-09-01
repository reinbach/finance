import json
import pytest

from sqlalchemy.exc import IntegrityError

from finance.models.account import Account, db
from finance.models.account_type import AccountType


class TestAccountModel():

    def setup_method(self, method):
        self.account_type = AccountType('Income')
        db.session.add(self.account_type)
        db.session.commit()

    def teardown_method(self, method):
        db.session.rollback()
        db.session.delete(self.account_type)
        db.session.commit()
        db.session.remove()

    def test_account_repr(self):
        """Ensure __repr__ function works"""
        a = Account('Bonus', self.account_type.account_type_id,
                    "Show me the money")
        assert repr(a) == '<Account: Bonus [Income]>'

    def test_account_add(self):
        """Test adding an account normaly"""
        a = Account("Salary", self.account_type.account_type_id,
                    "Show me the money")
        assert a.name == "Salary"

        db.session.add(a)
        db.session.commit()

        a2 = Account.query.filter(Account.name == a.name).first()
        assert a2.name == a.name
        assert a2.account_type == a.account_type
        assert a2.description == a.description
        assert bool(a2.account_id) is True

    def test_account_name_unique(self):
        """Test that account name uniqueness is maintained"""
        a = Account("Interest", self.account_type.account_type_id,
                    "Compound it baby")
        db.session.add(a)
        db.session.commit()

        with pytest.raises(IntegrityError):
            a2 = Account("Interest", self.account_type.account_type_id,
                         "No, don't charge me'")
            db.session.add(a2)
            db.session.commit()
        db.session.rollback()

    def test_account_jsonify(self):
        """Test the jsonify method"""
        a = Account("Interest", self.account_type.account_type_id,
                    "Compound it baby")
        assert dict == type(a.jsonify())
        assert bool(json.dumps(a.jsonify())) is True
