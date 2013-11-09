import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from finance.utils import Auth

app = Flask(__name__)
app.config.from_object(config)
app.auth = Auth()

db = SQLAlchemy(app)

import finance.views.base  # noqa
