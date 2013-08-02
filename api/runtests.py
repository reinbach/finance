import os
import sys
import unittest

import config

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance')
)

tests = unittest.TestLoader().discover(start_dir="tests")
suite = unittest.TestSuite(tests)
runner = unittest.TextTestRunner()

def main():
    import database
    database.init_db()
    runner.run(suite)
    database.drop_db()

if __name__ == "__main__":
    config.TESTING = True
    main()
