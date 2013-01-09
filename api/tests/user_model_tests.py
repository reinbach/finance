import unittest

from sqlalchemy.exc import IntegrityError

from finance.models import User, db_session

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        #self.app = finance.app.test_client()
        pass

    def tearDown(self):
        db_session.remove()

    def test_user_add(self):
        """Test adding a user normally"""
        u = User(name='Test', email='test@example.com')
        self.assertEqual(u.name, "Test")

        db_session.add(u)
        db_session.commit()

        u2 = User.query.filter(User.name == u.name).first()
        self.assertEqual(u2.name, u.name)
        self.assertEqual(u2.email, u.email)
        self.assertTrue(u2.user_id)

    def test_user_name_unique(self):
        """Test user name uniqueness is maintained"""
        u = User(name='Test_Unique', email='test1@example.com')
        db_session.add(u)
        db_session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "users_name_key"'
        ):
            u2 = User(name='Test_Unique', email='test1_@example.com')
            db_session.add(u2)
            db_session.commit()

    def test_user_email_unique(self):
        """Test user email uniqueness is maintained"""
        u = User(name='Test2', email='test_unique@example.com')
        db_session.add(u)
        db_session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "users_email_key"'
        ):
            u2 = User(name='Test2_', email='test_unique@example.com')
            db_session.add(u2)
            db_session.commit()


test_cases = [
    UserModelTestCase
]