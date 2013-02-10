from wtforms import TextField, validators

from finance.forms import BaseForm
from finance.models import AccountType

class AccountTypeForm(BaseForm):
    name = TextField(
        'Name',
        [validators.Length(min=4, max=20), validators.Required()]
    )

    def __init__(self, *args, **kwargs):
        self.account_type_id = None
        if kwargs.get('account_type_id', False):
            self.account_type_id = kwargs.pop('account_type_id')
        super(AccountTypeForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        acct_type = AccountType.query.filter(
            AccountType.name == field.data, AccountType.account_type_id != self.account_type_id
        ).first()
        if acct_type:
            raise validators.ValidationError('Name needs to be unique.')

