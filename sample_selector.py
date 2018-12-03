#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import gzip


# In[23]:


Z_FILE = 'primary_table.csv'
HST_FILE = 'hst_table.csv.gz'
SPITZ_FILE = 'sha_table.csv'
SWIFT_FILE = 'swift_table.csv'


# In[21]:


# grbs with redshift
z_grbs = set()
with open(Z_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            z = float(row['z'])
        # only accept "valid" redshifts
        except ValueError:
            continue
        z_grbs.add(row['grb'])


# In[24]:


# grbs observed in Spitzer
spitz_grbs = set()
with open(SPITZ_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        spitz_grbs.add(row['grb'])


# In[121]:


def date_checker(grb, start_time, nmonths=4):
    start_mm = int(start_time.split('/')[0])
    start_yy = int(start_time.split('/')[-1].split(' ')[0][2:])

    grb_mm = int(grb[2:4])
    grb_yy = int(grb[0:2])
    late_enough = True
    if start_yy == grb_yy + 1:
        if 12 - grb_mm - start_mm < nmonths:
            late_enough = False
    elif start_yy == grb_yy:
        if grb_mm - start_mm < nmonths:
            late_enough = False
    return late_enough


# In[122]:


# grbs observed in HST
hst_grbs = set()
with gzip.open(HST_FILE, 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if date_checker(row['grb'], row['StartTime'], nmonths=4):
            hst_grbs.add(row['grb'])

