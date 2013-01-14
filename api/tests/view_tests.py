import base64
import unittest

import finance

from finance.models import User, db_session

class BaseViewTestCase(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'secret'
        self.user = User(self.username, self.password)
        db_session.add(self.user)
        db_session.commit()
        self.app = finance.app.test_client()

    def tearDown(self):
        db_session.delete(self.user)
        db_session.commit()
        db_session.remove()

    def open_with_auth(self, url, method, username, password, data=None):
        return self.app.open(
            url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(
                    username + ":" + password
                )
            },
            data=data,
            follow_redirects=True
        )
