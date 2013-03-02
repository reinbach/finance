import datetime
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
        self.trx1 = Transaction(
            self.acct_bank.account_id,
            self.acct_expense1.account_id,
            5,
            'Interest Expense',
            datetime.date(2013, 2, 19)
        )
        self.trx2 = Transaction(
            self.acct_income1.account_id,
            self.acct_bank.account_id,
            5,
            'Interest Income',
            datetime.date(2013, 2, 19)
        )
        db_session.add(self.trx1)
        db_session.add(self.trx2)
        db_session.commit()

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
        db_session.delete(self.trx1)
        db_session.delete(self.trx2)

        db_session.commit()
        db_session.remove()


    def test_file_parse(self):
        """Test able to parse file"""
        trx_import = TransactionsImport(self.acct_bank.account_id, self.filename)
        self.assertEqual(trx_import.transactions, [])

        trx_import.parse_file()
        self.assertEqual(len(trx_import.transactions), 18)
        self.assertIn(
            {
                'date': '02/24/2013',
                'summary': "SHAWNEE PEAK",
                'amount': '24.00',
                'debit': None,
                'credit': self.acct_bank.account_id,
                'duplicate': False
            },
            trx_import.transactions
        )
        self.assertIn(
            {
                'date': '02/19/2013',
                'summary': "Interest Income",
                'amount': '5.00',
                'debit': self.acct_bank.account_id,
                'credit': self.acct_income1.account_id,
                'duplicate': True
            },
            trx_import.transactions
        )

    def test_setting_accounts(self):
        """Test setting accounts"""
        trx = {
            'summary': 'Salary',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.acct_bank.account_id, self.filename)
        trx_import.set_accounts(trx)

        self.assertEqual(self.acct_bank.account_id, trx['debit'])
        self.assertIsNone(trx['credit'])

        trx = {
            'summary': 'Office Expenses',
            'amount': '-10.00',
            'date': '02/19/2013'
        }
        trx_import.set_accounts(trx)
        self.assertEqual(self.acct_bank.account_id, trx['credit'])
        self.assertIsNone(trx['debit'])

    def test_get_account_none(self):
        """Test getting non existant account"""
        trx = {
            'summary': 'Salary',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.acct_bank.account_id, self.filename)
        res = trx_import.get_account(trx['summary'])
        self.assertIsNone(res)

    def test_get_account(self):
        """Test getting a valid account"""
        trx = {
            'summary': 'Interest Expense',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.acct_bank.account_id, self.filename)

        res = trx_import.get_account(trx['summary'])
        self.assertEqual(self.acct_expense1.account_id, res)

        trx = {
            'summary': 'Interest Income',
            'amount': '-5.00',
            'date': '02/19/2013'
        }
        res = trx_import.get_account(trx['summary'])
        self.assertEqual(self.acct_income1.account_id, res)

    def test_is_duplicate(self):
        """Test if trx is duplicate"""
        trx_import = TransactionsImport(self.acct_bank.account_id, self.filename)

        # no fields matching
        trx = {
            'summary': 'Interest',
            'amount': '5.01',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # only summary field matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.01',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # summary and amount fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.00',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # only summary and date fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.01',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # only amount and date fields matching
        trx = {
            'summary': 'Interest',
            'amount': '5.00',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # only date field matching
        trx = {
            'summary': 'Interest',
            'amount': '5.01',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertFalse(res)

        # all fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.00',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        self.assertTrue(res)



test_cases = [
    TrxImportTestCase,
]