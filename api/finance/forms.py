from wtforms import Form, DateField, DecimalField, IntegerField, TextField, validators

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

class TransactionForm(Form):
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