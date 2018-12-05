from numpy import loadtxt, savetxt
from time import time
from math import ceil

MAX_TARGETS = 500
SHA_FILE_PREFIX = 'sha/sha_query_table_{}'.format(int(time()))
PRIMARY_FILE = 'primary_table.csv'
HEADER = """COORD_SYSTEM: Equatorial
# Equatorial, Galactic, or Ecliptic - default is Equatorial
EQUINOX: J2000
# B1950, J2000, or blank for Galactic - default is J2000
NAME-RESOLVER: NED
# NED  Simbad - default is Simbad
#Name       RA/LON      DEC/LAT     PM-RA   PM-DEC  EPOCH"""

grb_data = loadtxt(
    PRIMARY_FILE, dtype=str, delimiter=',', usecols=(0,1), skiprows=1)
n_grbs = len(grb_data)

for i in range(n_grbs):
    grb_data[i, 0] = 'GRB{}'.format(grb_data[i, 0]).replace('S','')
    grb_data[i, 1] = grb_data[i, 1].replace("'", "m").replace(' ', '\t')

n_files = ceil(n_grbs/MAX_TARGETS)
start  = 0
for page in range(n_files):
    SHA_FILE = '{}_{}.txt'.format(SHA_FILE_PREFIX, page)
    end = start + MAX_TARGETS
    if end > n_grbs:
        end = n_grbs
    savetxt(
        SHA_FILE, grb_data[start:end], delimiter='\t', header=HEADER, fmt='%s',
        comments='')
    start = end
