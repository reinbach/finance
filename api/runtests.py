import os
import sys
import unittest

import finance
import config

sys.path.append(os.path.abspath(__file__))

test_modules = [
    'tests.user_model_tests',
]

suites = []
for test_mod in test_modules:
    _tmp = __import__(test_mod, globals(), locals(), ['test_cases'], -1)
    for test_case in _tmp.test_cases:
        suites.append(
            unittest.TestLoader().loadTestsFromTestCase(test_case)
        )

alltests = unittest.TestSuite(suites)
runner = unittest.TextTestRunner()

if __name__ == "__main__":
    config.TESTING = True
    finance.database.init_db()
    runner.run(alltests)
    finance.database.drop_db()