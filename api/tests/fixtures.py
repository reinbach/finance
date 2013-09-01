import datetime
import pytest

from finance import db
from finance.models.account import Account
from finance.models.account_type import AccountType
from finance.models.transaction import Transaction
from finance.models.user import User

db.init_db()


@pytest.fixture
def filename():
    return 'tests/trx_import_file_sample.csv'


def setup_user():
    username = 'admin'
    password = 'secret'
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return user, username, password


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    db.session.remove()


def setup_account_types():
    # setup account types
    assets = AccountType('Assets')
    income = AccountType('Income')
    expense = AccountType('Expense')
    db.session.add(assets)
    db.session.add(income)
    db.session.add(expense)
    db.session.commit()

    return {'assets': assets, 'income': income, 'expense': expense}


def setup_accounts(account_types):
    # setup accounts
    acct_bank = Account("Bank", account_types['assets'].account_type_id)
    acct_expense = Account("Expense1",
                           account_types['expense'].account_type_id)
    acct_income = Account("Income1", account_types['income'].account_type_id)
    db.session.add(acct_bank)
    db.session.add(acct_expense)
    db.session.add(acct_income)
    db.session.commit()

    return {'bank': acct_bank, 'expense': acct_expense, 'income': acct_income}


def setup_transactions(accounts):
    # setup transactions
    trx1 = Transaction(
        accounts['bank'].account_id,
        accounts['expense'].account_id,
        5,
        'Interest Expense',
        datetime.date(2013, 2, 19)
    )
    trx2 = Transaction(
        accounts['income'].account_id,
        accounts['bank'].account_id,
        5,
        'Interest Income',
        datetime.date(2013, 2, 19)
    )
    db.session.add(trx1)
    db.session.add(trx2)
    db.session.commit()

    return {'trx1': trx1, 'trx2': trx2}


def teardown(data):
    # remove account types
    for d in data:
        for r in d.values():
            db.session.delete(r)

    db.session.commit()
    db.session.remove()
