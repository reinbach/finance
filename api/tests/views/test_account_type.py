import json

from finance.models.account_type import AccountType, db_session
from tests.views.test_base import BaseViewTestCase


class AccountTypeViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(AccountTypeViewTestCase, self).setUp()
        self.account_type = AccountType('Expense')
        db_session.add(self.account_type)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.account_type)
        super(AccountTypeViewTestCase, self).tearDown()

    def test_view_auth_required(self):
        """Test that authentication is required"""
        rv = self.app.get("/account/types")
        self.assertEqual(401, rv.status_code)

    def test_view_all(self):
        """Test viewing all account types"""
        rv = self.open_with_auth(
            "/account/types",
            'GET',
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        acct_type = self.account_type.jsonify()
        self.assertIn(acct_type, data)

    def test_view_account_type(self):
        """Test viewing a single account type"""
        rv = self.open_with_auth(
            "/account/types/%s" % self.account_type.account_type_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(self.account_type.jsonify(), json.loads(rv.data))

    def test_view_account_type_404(self):
        """Test viewing a non-existant account type"""
        rv = self.open_with_auth(
            "/account/types/999",
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)
        self.assertIn("404 Not Found", rv.data)

    def test_view_add(self):
        """Test adding an account type"""
        name = 'Supplies'
        rv = self.open_with_auth(
            "/account/types",
            "POST",
            self.username,
            self.password,
            data=dict(
                name=name,
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

        acct_type = json.loads(rv.data)
        rv = self.open_with_auth(
            "/account/types/%s" % acct_type.get('account_type_id'),
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        acct_type_get = json.loads(rv.data)
        self.assertEqual(name, acct_type_get.get('name'))
        self.assertEqual(acct_type.get('account_type_id'),
                         acct_type_get.get('account_type_id'))

    def test_view_add_fail_invalid(self):
        """Test adding an invalid account type"""
        name = 'Sup'
        rv = self.open_with_auth(
            "/account/types",
            "POST",
            self.username,
            self.password,
            data=dict(
                name=name,
            )
        )
        self.assertEqual(400, rv.status_code)
        self.assertIn('errors', rv.data)

    def test_view_add_fail_unique(self):
        """Test adding a duplicate account type"""
        name = self.account_type.name
        rv = self.open_with_auth(
            "/account/types",
            "POST",
            self.username,
            self.password,
            data=dict(
                name=name,
            )
        )
        self.assertEqual(400, rv.status_code)
        self.assertIn('errors', rv.data)

    def test_view_delete(self):
        """Test deleting account"""
        account_type1 = AccountType(
            'Entertainment',
        )
        db_session.add(account_type1)
        db_session.commit()
        rv = self.open_with_auth(
            "/account/types/%s" % account_type1.account_type_id,
            "DELETE",
            self.username,
            self.password
        )
        self.assertEqual(200, rv.status_code)

        # attempt to get the account
        rv = self.open_with_auth(
            "/account/types/%s" % account_type1.account_type_id,
            "GET",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

    def test_view_delete_fail(self):
        """Test deleting a non existant account type"""
        rv = self.open_with_auth(
            "/account/types/999",
            "DELETE",
            self.username,
            self.password
        )
        self.assertEqual(404, rv.status_code)

    def test_view_update(self):
        """Test updating an account type"""
        name = 'Entertainment'
        account_type_id = self.account_type.account_type_id
        rv = self.open_with_auth(
            "/account/types/%s" % account_type_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name=name,
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

        rv = self.open_with_auth(
            "/account/types/%s" % account_type_id,
            "GET",
            self.username,
            self.password,
        )

        self.assertEqual(200, rv.status_code)
        acct_type_get = json.loads(rv.data)
        self.assertEqual(name, acct_type_get.get('name'))

    def test_view_update_nochange(self):
        """Test updating an account type with same name value"""
        account_type_id = self.account_type.account_type_id
        rv = self.open_with_auth(
            "/account/types/%s" % account_type_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name=self.account_type.name,
            )
        )
        self.assertEqual(200, rv.status_code)
        self.assertIn('Success', rv.data)

    def test_view_update_fail_invalid_id(self):
        """Test updating an account type with invalid id"""
        account_type_id = '999'
        rv = self.open_with_auth(
            "/account/types/%s" % account_type_id,
            "PUT",
            self.username,
            self.password,
            data=dict(
                name='Invalid',
            )
        )
        self.assertEqual(404, rv.status_code)

test_cases = [
    AccountTypeViewTestCase
]
