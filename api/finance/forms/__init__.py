import json

from wtforms import Form, TextField, validators
from werkzeug.datastructures import MultiDict


class BaseForm(Form):
    """Base Form Class

    We are not expecting to make use of request.form, but
    rather the request.data and we need to massage the data
    into a MultiDict format for things to work nicely

    We are only expecting a data param
    """
    def __init__(self, data):
        data = MultiDict(json.loads(data))
        super(BaseForm, self).__init__(data)


class UserForm(BaseForm):
    username = TextField('Username', [validators.Required()])
    password = TextField('Password', [validators.Required()])
