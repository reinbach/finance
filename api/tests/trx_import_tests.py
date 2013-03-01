import unittest

from finance.trx_import import TransactionsImport
from finance.models import Account, AccountType, Transaction, db_session

class TrxImportTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = 'tests/trx_import_file_sample.csv'

        # setup account types
        self.acct_type_assets = AccountType('Assets')
        self.acct_type_income = AccountType('Income')
        self.acct_type_expense = AccountType('Expense')
        db_session.add(self.acct_type_assets)
        db_session.add(self.acct_type_income)
        db_session.add(self.acct_type_expense)
        db_session.commit()

        # setup accounts
        self.acct_bank = Account("Bank", self.acct_type_assets.account_type_id)
        self.acct_expense1 = Account("Expense1", self.acct_type_expense.account_type_id)
        self.acct_income1 = Account("Income1", self.acct_type_income.account_type_id)
        db_session.add(self.acct_bank)
        db_session.add(self.acct_expense1)
        db_session.add(self.acct_income1)
        db_session.commit()

        # setup transactions

    def tearDown(self):
        # remove account types
        db_session.delete(self.acct_type_assets)
        db_session.delete(self.acct_type_income)
        db_session.delete(self.acct_type_expense)

        # remove accounts
        db_session.delete(self.acct_bank)
        db_session.delete(self.acct_expense1)
        db_session.delete(self.acct_income1)

        # remove transactions

        db_session.commit()
        db_session.remove()


    def test_file_parse(self):
        """Test able to parse file"""
        trximport = TransactionsImport(self.acct_bank.account_id, self.filename)
        self.assertEqual(trximport.transactions, [])

        trximport.parse_file()
        self.assertEqual(len(trximport.transactions), 18)

test_cases = [
    TrxImportTestCase,
]