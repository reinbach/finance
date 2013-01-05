from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from finance.database import metadata, db_session

class User(object):
    """User

    The users that can access the system
    """
    query = db_session.query_property()

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User: {0}>'.format(self.name)

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('email', String(120), unique=True)
)

mapper(User, users)


class Account(object):
    """Account

    The accounts all transactions happen in
    eg: Income, expense, assets and liabilities
    """

    query = db_session.query_property()

    def __init__(self, name=None, account_type=None, description=None):
        self.name = name
        self.account_type = account_type
        self.description = description

    def __repr__(self):
        return '<Account: {name} [{account_type}]>'.format(
            name=self.name,
            account_type=self.account_type
        )

    def balance(self):
        """Current balance of account"""
        # get a list of transactions and calculate it
        #TODO cache balance, and reset cache when new
        # transaction recorded for account
        return 0


class Transaction(object):
    """Transaction

    Record of the transaction
    """

    query = db_session.query_property()

    def __init__(
        self,
        account_debit=None,
        account_credit=None,
        amount=None,
        summary=None,
        description=None
    ):
        self.account_debit = account_debit
        self.account_credit = account_credit
        self.amount = amount
        self.summary = summary
        self.description = description

    def __repr__(self):
        #TODO determine account debit and then show amount in negative or positive
        # or think of a better short description of transaction to show
        return '<Transaction: {summary} {amount}>'.format(
            summary=self.summary,
            amount=self.amount
        )