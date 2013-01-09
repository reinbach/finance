import os
import sys
import unittest

import config

sys.path.append(os.path.abspath(__file__))

test_modules = [
    'tests.user_model_tests',
    'tests.account_model_tests',
    'tests.transaction_model_tests',
]

suites = []

def runTests():
    for test_mod in test_modules:
        _tmp = __import__(test_mod, globals(), locals(), ['test_cases'], -1)
        for test_case in _tmp.test_cases:
            suites.append(
                unittest.TestLoader().loadTestsFromTestCase(test_case)
            )

    alltests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(alltests)

def main():
    from finance import database
    database.init_db()
    runTests()
    database.drop_db()

if __name__ == "__main__":
    config.TESTING = True
    main()