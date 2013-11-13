import datetime
import json
import pytest

from sqlalchemy.exc import IntegrityError

from finance import db
from finance.models.account import Account
from finance.models.account_type import AccountType
from finance.models.transaction import Transaction


@pytest.fixture
def account_type(request):
    at = AccountType('Income')
    def fin():
        db.session.rollback()
        db.session.delete(at)
        db.session.commit()
        db.session.remove()
    db.session.add(at)
    db.session.commit()
    request.addfinalizer(fin)
    return at


@pytest.fixture
def trxs(request, account_type):
    at1 = AccountType("Assets")
    at2 = AccountType("Expenses")
    db.session.add(at1)
    db.session.add(at2)
    db.session.commit()

    a1 = Account("Checking", at1, "Small Bank")
    a2 = Account("Interest Income", account_type, "Compounding")
    a3 = Account("Groceries", at2, "Local")
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.commit()

    t1 = Transaction(a3, a1, 10.10, "Groceries", datetime.date.today())
    t2 = Transaction(a3, a1, 15.15, "Groceries", datetime.date.today())
    t3 = Transaction(a1, a2, 5.00, "Groceries", datetime.date.today())
    t4 = Transaction(a3, a1, 25.05, "Groceries", datetime.date.today())
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.add(t4)
    db.session.commit()

    def fin():
        db.session.rollback()
        db.session.delete(t1)
        db.session.delete(t2)
        db.session.delete(t3)
        db.session.delete(t4)
        db.session.delete(a1)
        db.session.delete(a2)
        db.session.delete(a3)
        db.session.delete(at1)
        db.session.delete(at2)
        db.session.commit()
        db.session.remove()

    request.addfinalizer(fin)

    return (a1, a2, a3)


class TestAccountModel():

    # def setup_method(self, method):
    #     self.account_type = AccountType('Income')
    #     db.session.add(self.account_type)
    #     db.session.commit()

    # def teardown_method(self, method):
    #     db.session.rollback()
    #     db.session.delete(self.account_type)
    #     db.session.commit()
    #     db.session.remove()

    def test_account_repr(self, account_type):
        """Ensure __repr__ function works"""
        a = Account('Bonus', account_type,
                    "Show me the money")
        assert repr(a) == '<Account: Bonus [Income]>'

    def test_account_add(self, account_type):
        """Test adding an account normaly"""
        a = Account("Salary", account_type,
                    "Show me the money")
        assert a.name == "Salary"

        db.session.add(a)
        db.session.commit()

        a2 = Account.query.filter(Account.name == a.name).first()
        assert a2.name == a.name
        assert a2.account_type == a.account_type
        assert a2.description == a.description
        assert bool(a2.account_id) is True

    def test_account_name_unique(self, account_type):
        """Test that account name uniqueness is maintained"""
        a = Account("Interest", account_type,
                    "Compound it baby")
        db.session.add(a)
        db.session.commit()

        with pytest.raises(IntegrityError):
            a2 = Account("Interest", account_type,
                         "No, don't charge me'")
            db.session.add(a2)
            db.session.commit()
        db.session.rollback()

    def test_account_jsonify(self, account_type):
        """Test the jsonify method"""
        a = Account("Interest", account_type,
                    "Compound it baby")
        assert dict == type(a.jsonify())
        assert bool(json.dumps(a.jsonify())) is True

    def test_transactions(self, trxs):
        """Test that account totals a list of transactions"""
        a1, a2, a3 = trxs
        assert len(a1.transactions()) == 4

    def test_get_total(self, trxs):
        """Test that account totals a list of transactions"""
        a1, a2, a3 = trxs
        assert a1.get_total(a1.credits) == 50.30

    def test_balance(self, trxs):
        a1, a2, a3 = trxs
        assert a1.get_balance() == -45.30