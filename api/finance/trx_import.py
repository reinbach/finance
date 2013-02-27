import csv

from decimal import Decimal

from finance.models import Transaction

class TransactionsImport():
    """Import transactions from csv file

    Expected format of file:
    Type, Trans Date, Post Date, Description, Amount

    Need to know which account these transactions are against.

    For each transaction in the file do;
    1. Does similar record exist in system?
     - does a record exist where summary equals description?
     - if so, use that same account for the other side of the transaction
    2. Is this transaction a duplicate?
     - does a record exist with the same post date and amount
     - mark as duplicate
    """

    def __init__(self, main_account, filename, *args, **kwargs):
        self.main_account = main_account
        self.filename = filename
        self.transactions = []

    def parse_file(self):
        """Parse file and create transactions"""
        with open(self.filename, 'rb') as fp:
            filereader = csv.DictReader(fp, delimiter=',')
            for trx in filereader:
                self.set_accounts(trx)
                trx.duplicate = self.is_duplicate(trx)
                self.transactions.append(trx)

    def set_accounts(self, trx):
        """Set debit/credit accounts for transaction"""
        other_account = self.get_account(trx['Description'])
        if Decimal(trx.amount) < 0:
            trx.credit = self.main_account
            trx.debit = other_account
        else:
            trx.debit = self.main_account
            trx.credit = other_account

    def get_account(self, summary):
        """Look for other side of transaction based on description"""
        return Transaction().query.filter(Transaction.summary == summary).first()

    def is_duplicate(self, trx):
        """Check whether transaction is a possible duplicate"""
        return bool(Transaction().query.filter(
            Transaction.summary == trx['Description'],
            Transaction.amount == trx['Amount'],
            Transaction.date == trx['Post Date']
        ).first())