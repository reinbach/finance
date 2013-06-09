from sqlalchemy import Table, Column, Integer, String

from werkzeug.security import generate_password_hash, check_password_hash

from finance import db_session
from finance.database import metadata

class User(object):
    """User

    The users that can access the system
    """
    query = db_session.query_property()

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {0}>'.format(self.username)

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('password_hash', String(100))
)
