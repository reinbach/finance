import csv

from decimal import Decimal

from finance.models.transaction import Transaction

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

    def __init__(self, main_account_id, filename, *args, **kwargs):
        self.main_account_id = main_account_id
        self.filename = filename
        self.transactions = []

    def parse_file(self):
        """Parse file and create transactions"""
        with open(self.filename, 'rb') as fp:
            filereader = csv.DictReader(fp, delimiter=',')
            for trx_import in filereader:
                trx = self.map_fields(trx_import)
                self.set_accounts(trx)
                trx['duplicate'] = self.is_duplicate(trx)
                self.transactions.append(trx)

    def map_fields(self, trx_import):
        """Map the respecitve fields"""
        return {
            'date': trx_import['Post Date'],
            'summary': trx_import['Description'],
            'amount': trx_import['Amount'],
        }

    def set_accounts(self, trx):
        """Set debit/credit accounts for transaction"""
        other_account_id = self.get_account(trx['summary'])
        if Decimal(trx['amount']) < 0:
            trx['credit'] = self.main_account_id
            trx['debit'] = other_account_id
        else:
            trx['debit'] = self.main_account_id
            trx['credit'] = other_account_id
        trx['amount'] = str(abs(Decimal(trx['amount'])))

    def get_account(self, summary):
        """Look for other side of transaction based on description"""
        res =  Transaction().query.filter(Transaction.summary == summary).first()

        if res is None:
            return None

        if res.debit.account_id == self.main_account_id:
            return res.credit.account_id
        return res.debit.account_id

    def is_duplicate(self, trx):
        """Check whether transaction is a possible duplicate"""
        return bool(Transaction().query.filter(
            Transaction.summary == trx['summary'],
            Transaction.amount == trx['amount'],
            Transaction.date == trx['date']
        ).first())