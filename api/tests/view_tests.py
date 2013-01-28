import base64
import json
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
            data=json.dumps(data),
            follow_redirects=True,
            content_type='application/json'
        )

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        return self.app.post(
            "/login",
            data=json.dumps(data),
            follow_redirects=True,
            content_type='application/json'
        )

    def logout(self, auth_token=None):
        return self.app.open(
            "/logout",
            'GET',
            headers={
                'Auth-Token': auth_token
            },
            follow_redirects=True
        )

class GeneralViewTestCase(BaseViewTestCase):

    def test_login(self):
        """Test logging in """
        rv = self.login(self.username, self.password)
        self.assertEqual(200, rv.status_code)
        res = json.loads(rv.data)
        self.assertIn("Success", res.get('message'))
        self.assertTrue('auth_token' in res)

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'Auth-Token': res.get('auth_token')
            }
        )
        self.assertEqual(200, rv.status_code)

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'Auth-Token': 'random'
            }
        )
        self.assertEqual(401, rv.status_code)

    def test_login_fail(self):
        """Test logging in with invalid credentials"""
        rv = self.login('boo', 'hoo')
        self.assertEqual(400, rv.status_code)
        self.assertIn('Invalid', json.loads(rv.data).get('message'))

    def test_logout(self):
        """Test logging out"""
        rv = self.login(self.username, self.password)
        self.assertEqual(200, rv.status_code)
        auth_token = json.loads(rv.data).get('auth_token')

        rv = self.logout(auth_token)
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', json.loads(rv.data).get('message'))

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'Auth-Token': auth_token
            }
        )
        self.assertEqual(401, rv.status_code)

test_cases = [
    GeneralViewTestCase
]