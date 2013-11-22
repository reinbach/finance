import pytest

from finance.models.auth import AuthUser, db
from sqlalchemy.exc import IntegrityError


class TestUserModel():

    def test_user_repr(self):
        """Ensure __repr__ function works"""
        u = AuthUser('test', 'secret')
        assert repr(u) == "<User: test>"

    def test_user_add(self):
        """Test adding a user normally"""
        u = AuthUser('test', 'secret')
        assert u.username == "test"

        db.session.add(u)
        db.session.commit()

        u2 = AuthUser.query.filter(AuthUser.username == u.username).first()
        assert u2.username == u.username
        assert bool(u2.user_id) is True
        assert u2.password_hash == u.password_hash

    def test_user_name_unique(self):
        """Test user name uniqueness is maintained"""
        u = AuthUser('test_unique', 'secret')
        db.session.add(u)
        db.session.commit()

        with pytest.raises(IntegrityError):
            u2 = AuthUser('test_unique', 'secret')
            db.session.add(u2)
            db.session.commit()
        db.session.rollback()

    def test_user_password(self):
        """Test user password is hashed"""
        password = 'secret'
        u = AuthUser('test2', password)

        with pytest.raises(AttributeError):
            u.password

        assert bool(u.password_hash) is True
        assert u.password_hash != password
