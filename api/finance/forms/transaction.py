from wtforms import (DateField, DecimalField, IntegerField, TextField,
                     validators, FileField)

from finance.forms import BaseForm, Form
from finance.models.account import Account


class DateLocaleField(DateField):
    """Overload DateField to handle locale format, if applicable"""
    def process_formdata(self, valuelist):
        def scrub_date(value):
            if 'Z' == value[-1:] and len(value) > 10:
                value = value[:10]
            return value

        valuelist = [scrub_date(x) for x in valuelist]
        return super(DateLocaleField, self).process_formdata(valuelist)


def validate_account(form, field):
    try:
        field.account = Account.query.get(field.data)
    except:
        raise validators.ValidationError(
            "{0} is an invalid account".format(field.name)
        )


class TransactionForm(BaseForm):
    debit = IntegerField('Debit', [validators.Required(), validate_account])
    credit = IntegerField('Credit', [validators.Required(), validate_account])
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


class TransactionsImportForm(Form):
    main_account_id = IntegerField('Account',
                                   [validators.Required(), validate_account])
    transactions_file = FileField(u"Transaction File",
                                  [validators.regexp(u'\.csv$')])