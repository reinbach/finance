from flask import Flask

import config

from finance.database import DB
from finance.utils import Auth

app = Flask(__name__)
app.config.from_object(config)
app.auth = Auth()

db = DB()
app.db = db

import finance.views.base  # noqa

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
