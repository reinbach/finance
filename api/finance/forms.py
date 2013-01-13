from wtforms import Form, TextField, validators

class AccountForm(Form):
    name = TextField(
        'Name',
        [validators.Length(min=4, max=50), validators.Required()]
    )
    account_type = TextField(
        'Account Type',
        [validators.Length(min=4, max=20), validators.Required()]
    )
    description = TextField('Description', [validators.Length(min=0, max=250)])
