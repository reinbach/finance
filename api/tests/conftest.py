import finance
import os
import tempfile

DB = None


def pytest_configure():
    global DB
    DB, finance.app.config['DATABASE'] = tempfile.mkstemp()
    finance.app.config['DATABASE_URI'] = 'sqlite:///{0}'.format(
        finance.app.config['DATABASE']
    )
    finance.app.config['TESTING'] = True
    from finance.models.auth import AuthUser  # noqa
    finance.db.create_all()


def pytest_unconfigure():
    global DB
    os.close(DB)
    os.unlink(finance.app.config['DATABASE'])
