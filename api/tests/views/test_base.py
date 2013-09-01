import base64
import json

from finance import app
from tests.fixtures import setup_user, delete_user


class BaseViewTestCase():

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
                'AuthToken': auth_token
            },
            follow_redirects=True
        )


class TestGeneralView(BaseViewTestCase):

    @classmethod
    def setup_class(self):
        self.user, self.username, self.password = setup_user()
        self.app = app.test_client()

    @classmethod
    def teardown_class(self):
        delete_user(self.user)

    def test_version(self):
        """Test version number"""
        rv = self.app.get("/")
        assert 200 == rv.status_code
        assert 'version' in json.loads(rv.data)

    def test_login(self):
        """Test logging in """
        rv = self.login(self.username, self.password)
        assert 200 == rv.status_code
        res = json.loads(rv.data)
        assert "Success" in res.get('message')
        assert 'auth_token' in res

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'AuthToken': res.get('auth_token')
            }
        )
        assert 200 == rv.status_code

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'AuthToken': 'random'
            }
        )
        assert 401 == rv.status_code

    def test_login_fail(self):
        """Test logging in with invalid credentials"""
        rv = self.login('boo', 'hoo')
        assert 400 == rv.status_code
        assert 'Invalid' in json.loads(rv.data).get('message')

    def test_login_invalid(self):
        """Test logging in with invalid form post"""
        rv = self.app.post(
            "/login",
            data=json.dumps({"username": "admin"}),
            follow_redirects=True,
            content_type='application/json'
        )
        assert 400 == rv.status_code
        assert {
            u'password': [u'This field is required.']
        } == json.loads(rv.data)

    def test_logout(self):
        """Test logging out"""
        rv = self.login(self.username, self.password)
        assert 200 == rv.status_code
        auth_token = json.loads(rv.data).get('auth_token')

        rv = self.logout(auth_token)
        assert 200 == rv.status_code
        assert 'Success' in json.loads(rv.data).get('message')

        rv = self.app.open(
            "/accounts",
            'GET',
            headers={
                'AuthToken': auth_token
            }
        )
        assert 401 == rv.status_code
