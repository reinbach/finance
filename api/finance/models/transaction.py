from sqlalchemy import Table, Column, Date, Float, ForeignKey, Integer, String

from finance import db_session
from finance.database import metadata


class Transaction(object):
    """Transaction

    Record of the transaction
    """

    query = db_session.query_property()

    def __init__(
        self,
        account_debit_id=None,
        account_credit_id=None,
        amount=None,
        summary=None,
        date=None,
        description=None
    ):
        self.account_debit_id = account_debit_id
        self.account_credit_id = account_credit_id
        self.amount = amount
        self.summary = summary
        self.date = date
        self.description = description

    def __repr__(self):
        #TODO determine account debit and then show amount in negative or positive
        # or think of a better short description of transaction to show
        return '<Transaction: {summary} {amount}>'.format(
            summary=self.summary,
            amount=self.amount
        )

    def jsonify(self):
        res = {
            'transaction_id': self.transaction_id,
            'account_debit_id': self.account_debit_id,
            'account_credit_id': self.account_credit_id,
            'amount': self.amount,
            'summary': self.summary,
            'description': self.description,
            'date': self.date.strftime("%Y-%m-%d")
        }

        if self.debit is not None:
            res['debit'] = self.debit.jsonify()

        if self.credit is not None:
            res['credit'] = self.credit.jsonify()

        # balance may be set as a running total for an account
        if hasattr(self, 'balance'):
            res['balance'] = self.balance

        return res


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
