#!/usr/bin/env python
# coding: utf-8

# In[24]:


import re
import csv
import gzip
import dateutil
import matplotlib.pyplot as plt


# In[2]:


Z_FILE = 'primary_table.csv'
HST_FILE = 'hsc/hsc_results_table.csv.gz'
SPITZ_FILE = 'sha/sha_results_table_1543989340.csv'
SWIFT_FILE = 'swift_table.csv'


# In[3]:


# check if a grb has been observed nmonths after burst
def date_checker(grb, obs_time, nmonths=6):
    # grb string, e.g. 040924
    grb_num = re.sub('[^0-9]', '', grb)
    if grb.startswith('9'):
        grb_date_str = '19{}'.format(grb_num)
    else:
        grb_date_str = '20{}'.format(grb_num)
    
    grb_date = dateutil.parser.parse(grb_date_str)
    obs_date = dateutil.parser.parse(obs_time)
    relative = dateutil.relativedelta.relativedelta(months=nmonths)
    
    return obs_date > grb_date + relative


# In[4]:


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


# In[5]:


# grbs observed in Spitzer
spitz_grbs = set()
with open(SPITZ_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        grb = row['Search_Tgt'].strip('GRB')
        obs_date = row['reqendtime']
        
        is_late_enough = date_checker(grb, obs_date, nmonths=4)       
        if is_late_enough:
            spitz_grbs.add(grb)


# In[20]:


# grbs observed in HST
hst_grbs = set()
# hsc results indexed by primary_table since queries are 
# made from primary_table (parsed)
with open(Z_FILE, 'r') as f:
    grb_list = f.readlines()


with gzip.open(HST_FILE, 'rt') as f:
    reader = csv.DictReader(f)
    next(reader)     # skip dtype header
    for row in reader:
        entry = int(row['Entry'])
        grb = grb_list[entry].split(',')[0]
        obs_date = row['StopTime']
        if grb in hst_grbs:
            continue
        is_grb_target = 'grb' in row['Target Name'].lower()
        is_near = float(row["Ang Sep (')"]) < 5    # dist in arcmin
        is_late_enough = date_checker(grb, obs_date, nmonths=6)        
        if (is_grb_target or is_near) and is_late_enough:
            hst_grbs.add(grb)


# In[21]:


print(len(hst_grbs), len(spitz_grbs), len(z_grbs))


# In[22]:


# This is problematic. Must compare against current sample
# Issue from making angular separation too stringent in hsc search
print(len(z_grbs.intersection(spitz_grbs).intersection(hst_grbs)))


# In[ ]:


# plotter goes here

