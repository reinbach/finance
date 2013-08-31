import json

from finance.models.account import Account, db
from finance.models.account_type import AccountType
from tests.views.test_base import BaseViewTestCase


class AccountViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(AccountViewTestCase, self).setUp()
        self.account_type = AccountType('Expense')
        db.session.add(self.account_type)
        db.session.commit()
        self.account = Account('Insurance', self.account_type.account_type_id,
                               "Safety Net")
        db.session.add(self.account)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.account_type)
        db.session.delete(self.account)
        super(AccountViewTestCase, self).tearDown()

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/accounts")
        self.assertEqual(401, rv.status_code)

    def test_view_all(self):
        """Test viewing all accounts"""
        rv = self.open_with_auth(
            "/accounts",
            'GET',
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        acct = self.account.jsonify()
        self.assertIn(acct, data)

    def test_view_account(self):
        """Test viewing a single account"""
        rv = self.open_with_auth(
            "/accounts/%s" % self.account.account_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(self.account.jsonify(), json.loads(rv.data))

    def test_view_account_404(self):
        """Test viewing a non-existant account"""
        rv = self.open_with_auth(
            "/accounts/999",
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)
        self.assertIn("404 Not Found", rv.data)

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
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

        acct = json.loads(rv.data)
        rv = self.open_with_auth(
            "/accounts/%s" % acct.get('account_id'),
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        acct_get = json.loads(rv.data)
        self.assertEqual(name, acct_get.get('name'))
        self.assertEqual(account_type_json, acct_get.get('account_type'))
        self.assertEqual(account_type_json.get('account_type_id'),
                         acct_get.get('account_type_id'))
        self.assertEqual(description, acct_get.get('description'))
        self.assertEqual(acct.get('account_id'), acct_get.get('account_id'))

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
        self.assertEqual(400, rv.status_code)
        self.assertIn('errors', rv.data)

    def test_view_delete(self):
        """Test deleting account"""
        account1 = Account(
            'Entertainment',
            self.account_type.account_type_id,
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
        self.assertEqual(200, rv.status_code)

        # attempt to get the account
        rv = self.open_with_auth(
            "/accounts/%s" % account1.account_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

    def test_view_delete_fail(self):
        """Test deleting a non existant account"""
        rv = self.open_with_auth(
            "/accounts/999",
            "DELETE",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

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
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

        rv = self.open_with_auth(
            "/accounts/%s" % account_id,
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        acct_get = json.loads(rv.data)
        self.assertEqual(name, acct_get.get('name'))

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
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

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
        self.assertEqual(404, rv.status_code)
