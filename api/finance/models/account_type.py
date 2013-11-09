from finance import db


class AccountType(db.Model):
    """Account Type"""

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<AccountType: {name}>'.format(
            name=self.name
        )

    def jsonify(self):
        return {
            'account_type_id': self.pk,
            'name': self.name,
        }
