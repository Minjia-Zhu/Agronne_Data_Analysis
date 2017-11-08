"""
1. Insert a new column (State_code) based on Filename value
2. Cconcate all data for different states in to one dataframe and save it as csv 

"""

import csv
import glob
import pandas as pd 

path = r"/Users/minjiazhu/Desktop/Solar_pollination/CDL_buffer_data/csv" 
 
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    state_code = file_.split('_')[-1].split(".")[0]    
    df['State_code'] = state_code
    list_.append(df)
frame = pd.concat(list_)
frame.to_csv('all_states_gis_buffer.csv')