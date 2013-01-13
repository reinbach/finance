from sqlalchemy import Table, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from finance import db_session
from finance.database import metadata

class User(object):
    """User

    The users that can access the system
    """
    query = db_session.query_property()

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {0}>'.format(self.username)

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('password_hash', String(100))
)


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

    def jsonify(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'account_type': self.account_type,
            'description': self.description
        }

    def get_total(self, trx_list):
        """Get the sum of the relevant transactions"""
        total = 0
        for trx in trx_list:
            total += trx.amount
        return total

    def get_balance(self):
        """Current balance of account"""
        balance = self.get_total(self.debits) - self.get_total(self.credits)
        return balance

accounts = Table(
    'accounts',
    metadata,
    Column('account_id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('account_type', String(20)),
    Column('description', String(250)),
)


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
        description=None,
        date=None
    ):
        self.account_debit_id = account_debit.account_id
        self.account_credit_id = account_credit.account_id
        self.amount = amount
        self.summary = summary
        self.description = description
        self.date = date

    def __repr__(self):
        #TODO determine account debit and then show amount in negative or positive
        # or think of a better short description of transaction to show
        return '<Transaction: {summary} {amount}>'.format(
            summary=self.summary,
            amount=self.amount
        )

    def jsonify(self):
        return {
            'debit': self.account_debit_id,
            'credit': self.account_credit_id,
            'amount': self.amount,
            'summary': self.summary,
            'description': self.description,
            'date': self.date.strftime("%Y-%m-%d")
        }

transactions = Table(
    'transactions',
    metadata,
    Column('transaction_id', Integer, primary_key=True),
    Column('account_debit_id', Integer, ForeignKey('accounts.account_id')),
    Column('account_credit_id', Integer, ForeignKey('accounts.account_id')),
    Column('amount', Float(precision=2)),
    Column('summary', String(50)),
    Column('description', String(250)),
    Column('date', Date),
)

mapper(User, users)

mapper(
    Account,
    accounts,
    properties={
        'debits': relationship(Transaction, backref='debit', foreign_keys=[transactions.c.account_debit_id]),
        'credits': relationship(Transaction, backref='credit', foreign_keys=[transactions.c.account_credit_id]),
    }
)

mapper(Transaction, transactions)
