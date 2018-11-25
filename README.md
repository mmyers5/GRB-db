# GRB-db
.csv files for GRB database

To read:
```
import csv

# do `gzip -d hst_table.czv.gz`
hst_file = 'hst_table.csv'
hst_grbs = set()
with open(hst_file) as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    hst_grbs.add(row['grb'])
    
z_file = 'primary_table.csv'
with open(z_file) as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    if row['z']:
      z_grbs.add(row['grb'])
```

With the two sets `hst_grbs` and `z_grbs`, you can compare elements with `z_grbs.intersect(hst_grbs)`, which returns a set of common elements. Problems might arise from columns not having standardized data formats, but I think I covered 'em!
