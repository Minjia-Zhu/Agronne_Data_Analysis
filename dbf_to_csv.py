
"""
A tool to convert .dbf file to .csv file
Set path as the current working directory of your data folder 

"""
# Code adapted from :
#   https://gist.github.com/celisflen-bers/fe827aa724997b0487a084d225054e2c
#   https://stackoverflow.com/questions/18435983/batch-conversion-of-dbf-to-csv-in-python
#!/usr/bin/python

import csv
from dbfpy import dbf
import os
import sys

path = r"/Users/minjiazhu/Desktop/Solar_pollination/CDL_buffer_data" 

for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith('.dbf'):
            print ("Converting %s to csv" % filename)
            csv_fn = filename[:-4]+ ".csv"
            with open(csv_fn,'wb') as csvfile:
                in_db = dbf.Dbf(os.path.join(dirpath, filename))
                out_csv = csv.writer(csvfile)
                names = []
                for field in in_db.header.fields:
                    names.append(field.name)
                out_csv.writerow(names)
                for rec in in_db:
                    out_csv.writerow(rec.fieldData)
                in_db.close()
                print ("Done...")
        else:
          print ("Filename does not end with .dbf")
