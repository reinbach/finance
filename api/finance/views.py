import json

from flask.views import MethodView

import utils

from models import Account

class AccountAPI(MethodView):
    """Account Views"""

    decorators = [utils.requires_auth]

    def get(self, account_id):
        if account_id is None:
            # return a list of accounts
            pass
        else:
            # expose a single account
            return json.dumps(Account.query.all())

    def post(self):
        # create a new account
        pass

    def delete(self, account_id):
        # delete a single account
        pass

    def put(self, account_id):
        # update a single account
        pass

