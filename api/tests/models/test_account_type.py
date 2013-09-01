import json
import pytest

from sqlalchemy.exc import IntegrityError

from finance.models.account_type import AccountType, db


class TestAccountTypeModel():

    def test_account_type_repr(self):
        at = AccountType('Expenses')
        assert bool(at) is True

    def test_account_type_add(self):
        """Test adding an account type normally"""
        at = AccountType('Random')
        assert at.name == 'Random'

        db.session.add(at)
        db.session.commit()

        at2 = AccountType.query.filter(AccountType.name == at.name).first()
        assert at2.name == at.name
        assert bool(at2.account_type_id) is True

    def test_account_type_name_unique(self):
        """Test that account type name uniqueness is maintained"""
        at = AccountType('Interest Income')
        db.session.add(at)
        db.session.commit()

        with pytest.raises(IntegrityError):
            at2 = AccountType("Interest Income")
            db.session.add(at2)
            db.session.commit()
        db.session.rollback()

    def test_account_type_jsonify(self):
        """Test the jsonify method"""
        at = AccountType('Income')
        assert dict == type(at.jsonify())
        assert bool(json.dumps(at.jsonify())) is True
