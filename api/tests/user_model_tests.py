import os
import unittest
import tempfile

import finance

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, finance.app.config['DATABASE']['DB_NAME'] = tempfile.mkstemp()
        self.app = finance.app.test_client()
        finance.database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(finance.app.config['DATABASE']['DB_NAME'])

    def test_sample(self):
        assert True

test_cases = [
    UserModelTestCase
]