from finance import db
from finance.models.account_type import AccountType


class Account(db.Model):
    """Account

    The accounts all transactions happen in
    eg: Income, expense, assets and liabilities
    """

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(250))
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_type.pk'))
    account_type = db.relationship(AccountType,
                                   backref=db.backref('accounts',
                                                      lazy='dynamic'))

    def __init__(self, name=None, account_type=None, description=None):
        self.name = name
        self.account_type = account_type
        self.description = description

    def __repr__(self):
        return '<Account: {name} [{account_type}]>'.format(
            name=self.name,
            account_type=self.account_type.name
        )

    def jsonify(self):
        res = {
            'account_id': self.pk,
            'name': self.name,
            'account_type_id': self.account_type.pk,
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
        trx_list = list(self.debits) + list(self.credits)
        balance = 0
        for trx in trx_list:
            # remove duplicate information
            if self.pk == trx.account_debit.pk:
                balance += trx.amount
            else:
                balance -= trx.amount
            trx.balance = balance
        return trx_list
