from wtforms import TextField, validators

from finance.forms import BaseForm
from finance.models import AccountType

class AccountTypeForm(BaseForm):
    name = TextField(
        'Name',
        [validators.Length(min=4, max=20), validators.Required()]
    )

    def validate_name(form, field):
        if AccountType.query.filter(AccountType.name == field.data).first():
            raise validators.ValidationError('Name needs to be unique.')

