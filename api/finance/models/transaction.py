from finance import db
from finance.models.account import Account


class Transaction(db.Model):
    """Transaction

    Record of the transaction
    """

    transaction_id = db.Column(db.Integer, primary_key=True)
    account_debit_id = db.Column(db.Integer,
                                 db.ForeignKey('account.account_id'))
    account_debit = db.relationship(Account,
                                    foreign_keys=[account_debit_id],
                                    backref=db.backref('debits',
                                                       lazy='dynamic'))
    account_credit_id = db.Column(db.Integer,
                                  db.ForeignKey('account.account_id'))
    account_credit = db.relationship(Account,
                                     foreign_keys=[account_credit_id],
                                     backref=db.backref('credits',
                                                        lazy='dynamic'))
    amount = db.Column(db.Float(precision=2))
    summary = db.Column(db.String(50))
    description = db.Column(db.String(250))
    date = db.Column(db.Date)

    def __init__(
        self,
        account_debit=None,
        account_credit=None,
        amount=None,
        summary=None,
        date=None,
        description=None
    ):
        self.account_debit = account_debit
        self.account_credit = account_credit
        self.amount = amount
        self.summary = summary
        self.date = date
        self.description = description

    def __repr__(self):
        #TODO determine account debit and then show amount in
        # negative or positive
        # or think of a better short description of transaction to show
        return '<Transaction: {summary} {amount}>'.format(
            summary=self.summary,
            amount=self.amount
        )

    def jsonify(self):
        res = {
            'transaction_id': self.transaction_id,
            'account_debit_id': self.account_debit.account_id,
            'account_credit_id': self.account_credit.account_id,
            'amount': self.amount,
            'summary': self.summary,
            'description': self.description,
            'date': self.date.strftime("%Y-%m-%d")
        }

        if self.account_debit is not None:
            res['debit'] = self.account_debit.jsonify()

        if self.account_credit is not None:
            res['credit'] = self.account_credit.jsonify()

        # balance may be set as a running total for an account
        if hasattr(self, 'balance'):
            res['balance'] = self.balance

        return res
