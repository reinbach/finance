import json

from wtforms import Form, DateField, DecimalField, IntegerField, TextField, validators
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

class AccountTypeForm(BaseForm):
    name = TextField(
        'Name',
        [validators.Length(min=4, max=20), validators.Required()]
    )

class AccountForm(BaseForm):
    name = TextField(
        'Name',
        [validators.Length(min=4, max=50), validators.Required()]
    )
    account_type_id = IntegerField(
        'Account Type',
        [validators.Required()]
    )
    description = TextField('Description', [validators.Length(min=0, max=250)])

class TransactionForm(BaseForm):
    debit = IntegerField('Debit', [validators.Required()])
    credit = IntegerField('Credit', [validators.Required()])
    amount = DecimalField(
        'Amount',
        [validators.NumberRange(min=0), validators.Required()]
    )
    summary = TextField(
        'Summary',
        [validators.Length(min=3, max=50), validators.Required()]
    )
    date = DateField('Date', [validators.Required()])
    description = TextField('Description', [validators.Length(min=0, max=250)])