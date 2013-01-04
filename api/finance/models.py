from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from finance.database import metadata, db_session

class User(object):
    query = db_session.query_property()

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User: {0}>'.format(self.name)

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('email', String(120), unique=True)
)

mapper(User, users)