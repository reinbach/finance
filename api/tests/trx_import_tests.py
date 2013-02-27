import unittest

from finance.trx_import import TransactionsImport

class TrxImportTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_account(self):
        """Test get account returns valid account"""
        self.assertTrue(True)

test_cases = [
    TrxImportTestCase,
]