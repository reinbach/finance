import finance
import os
import tempfile

DB = None

def pytest_runtest_setup():
    global DB
    DB, finance.app.config['DATABASE'] = tempfile.mkstemp()
    finance.app.config['TESTING'] = True
    finance.db.create_all()

def pytest_runtest_teardown():
    global DB
    os.close(DB)
    os.unlink(finance.app.config['DATABASE'])
