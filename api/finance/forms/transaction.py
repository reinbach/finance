from wtforms import (DateField, DecimalField, IntegerField, TextField,
                     validators)

from finance.forms import BaseForm


class DateLocaleField(DateField):
    """Overload DateField to handle locale format, if applicable"""
    def process_formdata(self, valuelist):
        def scrub_date(value):
            if 'Z' == value[-1:] and len(value) > 10:
                value = value[:10]
            return value

        valuelist = [scrub_date(x) for x in valuelist]
        return super(DateLocaleField, self).process_formdata(valuelist)


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
    date = DateLocaleField('Date', [validators.Required()])
    description = TextField('Description', [validators.Length(min=0, max=250)])
