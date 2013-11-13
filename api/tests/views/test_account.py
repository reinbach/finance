import json

from finance import app, db
from finance.models.account import Account
from finance.models.account_type import AccountType
from tests.fixtures import setup_user, delete_user
from tests.views.test_base import BaseViewTestCase


class TestAccountView(BaseViewTestCase):

    def setup_method(self, method):
        self.user, self.username, self.password = setup_user()
        self.app = app.test_client()
        self.account_type = AccountType('Expense')
        db.session.add(self.account_type)
        db.session.commit()
        self.account = Account('Insurance', self.account_type,
                               "Safety Net")
        db.session.add(self.account)
        db.session.commit()

    def teardown_method(self, method):
        db.session.delete(self.account_type)
        db.session.delete(self.account)
        db.session.commit()
        delete_user(self.user)

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/accounts")
        assert 401 == rv.status_code

    def test_view_all(self):
        """Test viewing all accounts"""
        rv = self.open_with_auth(
            "/accounts",
            'GET',
            self.username,
            self.password
        )
        assert 200 == rv.status_code
        data = json.loads(rv.data)
        acct = self.account.jsonify()
        assert acct in data

    def test_view_account(self):
        """Test viewing a single account"""
        rv = self.open_with_auth(
            "/accounts/%s" % self.account.account_id,
            "GET",
            self.username,
            self.password
        )
        assert 200 == rv.status_code
        assert self.account.jsonify() == json.loads(rv.data)

    def test_view_account_404(self):
        """Test viewing a non-existant account"""
        rv = self.open_with_auth(
            "/accounts/999",
            "GET",
            self.username,
            self.password
        )
        assert 404 == rv.status_code
        assert "404 Not Found" in rv.data

    def test_view_add(self):
        """Test adding an account"""
        name = 'Supplies'
        account_type_json = self.account_type.jsonify()
        description = 'Getting things done'
        rv = self.open_with_auth(
            "/accounts",
            "POST",
            self.username,
            self.password,
            data=dict(
                name=name,
                account_type_id=account_type_json.get('account_type_id'),
                description=description
            )
        )
        assert 200 == rv.status_code
        assert 'Success' in rv.data

        acct = json.loads(rv.data)
        rv = self.open_with_auth(
            "/accounts/%s" % acct.get('account_id'),
            "GET",
            self.username,
            self.password,
        )

        assert 200 == rv.status_code
        acct_get = json.loads(rv.data)
        assert name == acct_get.get('name')
        assert account_type_json == acct_get.get('account_type')
        assert account_type_json.get('account_type_id') == \
            acct_get.get('account_type_id')
        assert description == acct_get.get('description')
        assert acct.get('account_id') == acct_get.get('account_id')

    def test_view_add_fail(self):
        """Test adding an invalid account"""
        name = 'Supplies'
        account_type = 'Exp'
        description = 'Getting things done'
        rv = self.open_with_auth(
            "/accounts",
            "POST",
            self.username,
            self.password,
            data=dict(
                name=name,
                account_type=account_type,
                description=description
            )
        )
        assert 400 == rv.status_code
        assert 'errors' in rv.data

    def test_view_delete(self):
        """Test deleting account"""
        account1 = Account(
            'Entertainment',
            self.account_type,
            "Party like it's 1999'"
        )
        db.session.add(account1)
        db.session.commit()
        rv = self.open_with_auth(
            "/accounts/%s" % account1.account_id,
            "DELETE",
            self.username,
            self.password
        )
        assert 200 == rv.status_code

        # attempt to get the account
        rv = self.open_with_auth(
            "/accounts/%s" % account1.account_id,
            "GET",
            self.username,
            self.password
        )
        assert 404 == rv.status_code

    def test_view_delete_fail(self):
        """Test deleting a non existant account"""
        rv = self.open_with_auth(
            "/accounts/999",
            "DELETE",
            self.username,
            self.password
        )
        assert 404 == rv.status_code

    def test_view_update(self):
        """Test updating an account"""
        name = 'Entertainment'
        account_id = self.account.account_id
        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name=name,
                account_type_id=self.account.account_type_id,
                description=self.account.description
            )
        )
        assert 200 == rv.status_code
        assert 'Success' in rv.data

        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            "GET",
            self.username,
            self.password,
        )

        assert 200 == rv.status_code
        acct_get = json.loads(rv.data)
        assert name == acct_get.get('name')

    def test_view_update_nonvalid(self):
        """Test updating an account with invalid form data"""
        name = ""
        account_id = self.account.account_id
        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            'PUT',
            self.username,
            self.password,
            data=dict(
                name=name,
                account_type_id=self.account.account_type_id,
                description=self.account.description,
            )
        )
        assert 400 == rv.status_code
        assert 'errors' in rv.data

    def test_view_update_nochange(self):
        """Test updating an account with same values"""
        account_id = self.account.account_id
        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name=self.account.name,
                account_type_id=self.account.account_type_id,
                description=self.account.description
            )
        )
        assert 200 == rv.status_code
        assert 'Success' in rv.data

    def test_view_update_fail_invalid_id(self):
        """Test updating an account with invalid id"""
        account_id = '999'
        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name=self.account.name,
                account_type_id=self.account.account_type_id,
                description=self.account.description
            )
        )
        assert 404 == rv.status_code
