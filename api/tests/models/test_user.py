from sqlalchemy.exc import IntegrityError

from finance.models.user import User, db


class UserModelTestCase():

    @classmethod
    def teardown_class(self):
        db.session.remove()

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        u = User('test', 'secret')
        self.assertTrue(u)

    def test_user_add(self):
        """Test adding a user normally"""
        u = User('test', 'secret')
        self.assertEqual(u.username, "test")

        db.session.add(u)
        db.session.commit()

        u2 = User.query.filter(User.username == u.username).first()
        self.assertEqual(u2.username, u.username)
        self.assertTrue(u2.user_id)
        self.assertEqual(u2.password_hash, u.password_hash)

    def test_user_name_unique(self):
        """Test user name uniqueness is maintained"""
        u = User('test_unique', 'secret')
        db.session.add(u)
        db.session.commit()

        with self.assertRaisesRegexp(
            IntegrityError,
            'violates unique constraint "users_username_key"'
        ):
            u2 = User('test_unique', 'secret')
            db.session.add(u2)
            db.session.commit()

    def test_user_password(self):
        """Test user password is hashed"""
        password = 'secret'
        u = User('test2', password)

        with self.assertRaises(AttributeError):
            u.password
        self.assertTrue(u.password_hash)
        self.assertNotEqual(u.password_hash, password)
