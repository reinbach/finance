from greplin import scales

STATS = scales.collection(
    "/api",
    scales.IntStat('notfound'),
    scales.IntStat('validation'),
    scales.IntStat('errors'),
    scales.IntStat('success'),
    scales.PmfStat('get_account'),
    scales.PmfStat('all_accounts'),
    scales.PmfStat('add_account'),
    scales.PmfStat('delete_account'),
    scales.PmfStat('update_account'),
)
