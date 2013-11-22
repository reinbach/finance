import sys

from finance import db
from finance.models.auth import AuthUser
from finance.models.account import Account
from finance.models.account_type import AccountType


def create_db(args):
    print("Creating database...")
    db.create_all()
    print("done.")


def create_user(args):
    print("Creating user...")
    username = args[0] if len(args) > 0 else 'admin'
    password = args[1] if len(args) > 1 else 'secret'
    u = AuthUser(username, password)
    db.session.add(u)
    db.session.commit()
    print("done.")


def load_default_data(args):
    print("Loading default data...")

    # load account types
    asset = AccountType('Assets')
    liability = AccountType('Liability')
    income = AccountType('Income')
    expense = AccountType('Expense')
    db.session.add(asset)
    db.session.add(liability)
    db.session.add(income)
    db.session.add(expense)
    db.session.commit()
    print("done.")


COMMANDS = {
    'initdb': create_db,
    'user': create_user,
    'loaddata': load_default_data,
}

if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
    except KeyError:
        print("Missing required command\n")
        sys.exit(1)
    else:
        COMMANDS[cmd](sys.argv[2:])
