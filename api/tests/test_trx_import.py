from finance.trx_import import TransactionsImport
from fixtures import (filename, setup_accounts, setup_account_types,
                      setup_transactions, teardown)


class TestTrxImport():
    @classmethod
    def setup_class(self):
        self.filename = filename()
        self.account_types = setup_account_types()
        self.accounts = setup_accounts(self.account_types)
        self.transactions = setup_transactions(self.accounts)

    @classmethod
    def teardown_class(self):
        teardown([self.transactions, self.accounts, self.account_types])

    def test_file_parse(self):
        """Test able to parse file"""
        trx_import = TransactionsImport(self.accounts['bank'].account_id,
                                        self.filename)
        assert trx_import.transactions == []

        trx_import.parse_file()
        assert len(trx_import.transactions) == 18

        assert {
            'date': '02/24/2013',
            'summary': "SHAWNEE PEAK",
            'amount': '24.00',
            'debit': None,
            'credit': self.accounts['bank'].account_id,
            'duplicate': False
        } in trx_import.transactions

        assert {
            'date': '02/19/2013',
            'summary': "Interest Income",
            'amount': '5.00',
            'debit': self.accounts['bank'].account_id,
            'credit': self.accounts['income'].account_id,
            'duplicate': True
        } in trx_import.transactions

    def test_setting_accounts(self):
        """Test setting accounts"""
        trx = {
            'summary': 'Salary',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.accounts['bank'].account_id,
                                        self.filename)
        trx_import.set_accounts(trx)

        assert self.accounts['bank'].account_id == trx['debit']
        assert trx['credit'] is None

        trx = {
            'summary': 'Office Expenses',
            'amount': '-10.00',
            'date': '02/19/2013'
        }
        trx_import.set_accounts(trx)
        assert self.accounts['bank'].account_id == trx['credit']
        assert trx['debit'] is None

    def test_get_account_none(self):
        """Test getting non existant account"""
        trx = {
            'summary': 'Salary',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.accounts['bank'].account_id,
                                        self.filename)
        res = trx_import.get_account(trx['summary'])
        assert res is None

    def test_get_account(self):
        """Test getting a valid account"""
        trx = {
            'summary': 'Interest Expense',
            'amount': '10.00',
            'date': '02/19/2013'
        }
        trx_import = TransactionsImport(self.accounts['bank'].account_id,
                                        self.filename)

        res = trx_import.get_account(trx['summary'])
        assert self.accounts['expense'].account_id == res

        trx = {
            'summary': 'Interest Income',
            'amount': '-5.00',
            'date': '02/19/2013'
        }
        res = trx_import.get_account(trx['summary'])
        assert self.accounts['income'].account_id == res

    def test_is_duplicate(self):
        """Test if trx is duplicate"""
        trx_import = TransactionsImport(self.accounts['bank'].account_id,
                                        self.filename)

        # no fields matching
        trx = {
            'summary': 'Interest',
            'amount': '5.01',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # only summary field matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.01',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # summary and amount fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.00',
            'date': '02/18/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # only summary and date fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.01',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # only amount and date fields matching
        trx = {
            'summary': 'Interest',
            'amount': '5.00',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # only date field matching
        trx = {
            'summary': 'Interest',
            'amount': '5.01',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is False

        # all fields matching
        trx = {
            'summary': 'Interest Expense',
            'amount': '5.00',
            'date': '02/19/2013'
        }
        res = trx_import.is_duplicate(trx)
        assert res is True
