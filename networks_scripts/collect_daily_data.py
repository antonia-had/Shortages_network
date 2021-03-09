# finds daily user networks with interesting properties in a given year

import networkx as nx
import os
import pandas as pd
import csv
from datetime import datetime


def day_water_rights(date = '2002-09-09'):
    # returns .csv file showing all calls for a particular day
    # format date as YYYY-MM-DD string


    path = 'yearly_data/'
    years_list = os.listdir(path)
    years_list = years_list[1:] # removes .DS store file name

    for year in years_list:
       if date[:4] == year[:-4]:
           df = pd.read_csv(path + year, dtype=object, error_bad_lines=False)
           df = df.drop(df.columns[0], axis=1)
           new_df = df[df['analysisDate'].str.contains(date)]
           new_df.to_csv('daily_data/' + date + '.csv')
           break

#################################################################################################################

# create list of all date strings in YYYY-MM-DD format
# dates = pd.date_range(start="2000-01-01", end="2020-10-31")
dates = pd.date_range(start="2004-11-09", end="2020-10-31")
dates = [i.strftime('%Y-%m-%d') for i in dates]
print(dates)

for date in dates:
    print(date)
    day_water_rights(date)




