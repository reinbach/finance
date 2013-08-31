from sqlalchemy import Table, Column, ForeignKey, Integer, String

from finance import db
from finance.models.account_type import AccountType


class Account(object):
    """Account

    The accounts all transactions happen in
    eg: Income, expense, assets and liabilities
    """

    query = db.session.query_property()

    def __init__(self, name=None, account_type_id=None, description=None):
        self.name = name
        self.account_type_id = account_type_id
        self.description = description
        self.account_type = AccountType.query.get(self.account_type_id)

    def __repr__(self):
        return '<Account: {name} [{account_type}]>'.format(
            name=self.name,
            account_type=self.account_type.name
        )

    def jsonify(self):
        res = {
            'account_id': self.account_id,
            'name': self.name,
            'account_type_id': self.account_type_id,
            'description': self.description,
            'balance': self.get_balance(),
        }

        if self.account_type is not None:
            res['account_type'] = self.account_type.jsonify()

        return res

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

    def transactions(self):
        """Get all transactions associated with this account

        We want to clearly indicate the opposite account
        And maintain a running balance for each transaction
        """
        trx_list = self.debits + self.credits
        balance = 0
        for trx in trx_list:
            # remove duplicate information
            if self.account_id == trx.debit.account_id:
                balance += trx.amount
            else:
                balance -= trx.amount
            trx.balance = balance
        return trx_list

accounts = Table(
    'accounts',
    db.metadata,
    Column('account_id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('account_type_id', Integer,
           ForeignKey('account_types.account_type_id')),
    Column('description', String(250)),
)
