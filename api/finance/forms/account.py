from wtforms import IntegerField, TextField, validators

from finance.forms import BaseForm


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
