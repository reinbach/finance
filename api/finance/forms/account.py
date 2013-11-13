from wtforms import IntegerField, TextField, validators

from finance.forms import BaseForm
from finance.models.account_type import AccountType


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

    def validate_account_type_id(form, field):
        try:
            form.acct_type = AccountType.query.get(field.data)
        except:
            raise validators.ValidationError("Invalid Account Type")