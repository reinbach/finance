import datetime

from mock import Mock

from finance import app
from finance.utils import crossdomain
from tests.fixtures import setup_user, delete_user
from tests.views.test_base import BaseViewTestCase


class TestCrossDomain(BaseViewTestCase):

    @classmethod
    def setup_class(self):
        self.user, self.username, self.password = setup_user()
        self.app = app.test_client()

    @classmethod
    def teardown_class(self):
        delete_user(self.user)

    def test_init(self):
        c = crossdomain(origin=['example.com', 'www.example.com'],
                        methods=['GET', 'POST'], headers=['Basic'],
                        max_age=datetime.timedelta(days=1))
        func = Mock(__name__='mock_func')
        c(func)

    # def test_options_method(self):
    #     rv = self.app.get("/", method="OPTIONS")
    #     assert rv.status_code == 204
