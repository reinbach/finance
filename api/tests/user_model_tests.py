import unittest

import finance

from finance.models import User
from finance.database import get_db_session

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = finance.app.test_client()
        self.db_session = get_db_session()

    def tearDown(self):
        pass

    def test_user_add(self):
        """Test adding a user normally"""
        u = User(name='Test', email='test@example.com')
        self.db_session.add(u)
        self.db_session.commit()

    def test_user_id(self):
        """Test adding sets id correctly"""
        self.skipTest('holder')

    def test_user_name_unique(self):
        """Test user name uniqueness is maintained"""
        self.skipTest('holder')

    def test_user_email_unique(self):
        """Test user email uniqueness is maintained"""
        self.skipTest('holder')


test_cases = [
    UserModelTestCase
]