from sqlalchemy import Table, Column, Integer, String

from finance import db_session
from finance.database import metadata


class AccountType(object):
    """Account Type"""

    query = db_session.query_property()

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<AccountType: {name}>'.format(
            name=self.name
        )

    def jsonify(self):
        return {
            'account_type_id': self.account_type_id,
            'name': self.name,
        }

account_types = Table(
    'account_types',
    metadata,
    Column('account_type_id', Integer, primary_key=True),
    Column('name', String(20), unique=True),
)
