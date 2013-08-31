import config

config.TESTING = True

from tests.fixtures import (filename, setup_account_types, setup_accounts,
                            setup_transactions)

__all__ = ['filename', 'setup_account_types', 'setup_accounts',
           'setup_transactions']
