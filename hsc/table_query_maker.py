import re
import pandas
from math import ceil

MAX_TARGETS = 1000
PRIMARY_TABLE = '../primary_table.csv'
SHA_TABLE = '../sha/sha_results_table_1543989340.csv'
QUERY_TABLE_PREFIX = 'sha_hla_query_table'

query_table = []

with open(PRIMARY_TABLE, 'r') as f:
    primary_df = pandas.read_csv(f)

with open(SHA_TABLE, 'r') as f:
    sha_df = pandas.read_csv(f)
sha_grbs = sha_df['Search_Tgt'].unique()

def hms_to_deg(hms):
    dims = 'hms'
    coords = {}
    for dim in dims:
        reg = re.compile('\d+{}'.format(dim))
        num = float(reg.findall(hms)[0].strip(dim))
        coords[dim] = num
    deg = (
        15 * coords['h']          # 15 degrees per hour
        + 15 * coords['m']/60.    # 60 minutes per hour
        + 15 * coords['s']/3600.  # 60 seconds per minute
    )
    return deg

def dm_to_deg(dm):
    dims = "dm"
    dm = dm.replace("'", "m")
    coords = {}
    for dim in dims:
        reg = re.compile('[\d.\+\-]+\d+{}'.format(dim))
        num = float(reg.findall(dm)[0].strip(dim))
        coords[dim] = num
    is_positive = coords['d'] > 0.
    if is_positive:
        deg = (
            coords['d']
            + coords['m']/60.
        )
    else:
        deg = (
            coords['d']
            - coords['m']/60.
        )
    return deg

for grb in primary_df['grb']:
    search_target = 'GRB{}'.format(grb)
    if search_target not in sha_grbs:
        radec = primary_df.loc[primary_df['grb'] == grb, 'radec'].iloc[0]
        hms, dm = radec.split(' ')    
        ra = hms_to_deg(hms)
        dec = dm_to_deg(dm)
    else:
        ra = sha_df.loc[
            sha_df['Search_Tgt'] == search_target, 'RA(J2000)'
        ].values[0]
        dec = sha_df.loc[
            sha_df['Search_Tgt'] == search_target, 'Dec(J2000)'
        ].values[0]
    query_table.append(
        '{ra},{dec},{grb}'.format(
            grb=search_target, ra=ra, dec=dec
        )
    )

n_grbs = len(query_table)
n_files = ceil(n_grbs/MAX_TARGETS)
start = 0
for page in range(n_files):
    query_table_file = '{}_{}.csv'.format(QUERY_TABLE_PREFIX, page)
    end = start + MAX_TARGETS
    if end > n_grbs:
        end = n_grbs
    with open(query_table_file, 'w') as f:
        f.write('\n'.join(query_table[start:end]))
    start = end
