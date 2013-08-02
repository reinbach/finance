from unittest import TestCase

from finance.utils import crossdomain

class TestCrossDomain(TestCase):
    def test_init_origin(self):
        c = crossdomain(origin=['example.com', 'www.example.com'])
        self.assertEqual(c.origin, 'example.com, www.example.com')

    def test_init_methods(self):
        c = crossdomain(methods=['GET', 'POST'])
        self.assertEqual(c.methods, 'GET, POST')


test_cases = [
    TestCrossDomain
]