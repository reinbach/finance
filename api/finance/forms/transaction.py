from wtforms import DateField, DecimalField, IntegerField, TextField, validators

from finance.forms import BaseForm

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