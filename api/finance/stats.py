from greplin import scales

STATS = scales.collection(
    "/api",
    scales.IntStat('notfound'),
    scales.IntStat('validation'),
    scales.IntStat('errors'),
    scales.IntStat('success'),

    # account types
    scales.PmfStat('get_account_type'),
    scales.PmfStat('all_account_types'),
    scales.PmfStat('add_account_type'),
    scales.PmfStat('delete_account_type'),
    scales.PmfStat('update_account_type'),

    # accounts
    scales.PmfStat('get_account'),
    scales.PmfStat('all_accounts'),
    scales.PmfStat('add_account'),
    scales.PmfStat('delete_account'),
    scales.PmfStat('update_account'),

    # transactions
    scales.PmfStat('get_transaction'),
    scales.PmfStat('all_transactions'),
    scales.PmfStat('add_transaction'),
    scales.PmfStat('delete_transaction'),
    scales.PmfStat('update_transaction'),

)
