import json

from flask.views import MethodView

import utils

class UserAPI(MethodView):
    """User Views"""

    decorators = [utils.user_required]

    def get(self, user_id):
        if user_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            return json.dumps({"users": [1, 2, 3]})

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

