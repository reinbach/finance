import pytest

from finance.models.user import User, db
from sqlalchemy.exc import IntegrityError


class TestUserModel():

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        u = User('test', 'secret')
        assert repr(u) == "<User: test>"

    def test_user_add(self):
        """Test adding a user normally"""
        u = User('test', 'secret')
        assert u.username == "test"

        db.session.add(u)
        db.session.commit()

        u2 = User.query.filter(User.username == u.username).first()
        assert u2.username == u.username
        assert bool(u2.pk) is True
        assert u2.password_hash == u.password_hash

    def test_user_name_unique(self):
        """Test user name uniqueness is maintained"""
        u = User('test_unique', 'secret')
        db.session.add(u)
        db.session.commit()

        with pytest.raises(IntegrityError):
            u2 = User('test_unique', 'secret')
            db.session.add(u2)
            db.session.commit()
        db.session.rollback()

    def test_user_password(self):
        """Test user password is hashed"""
        password = 'secret'
        u = User('test2', password)

        with pytest.raises(AttributeError):
            u.password

        assert bool(u.password_hash) is True
        assert u.password_hash != password
