# sorts all structure call analysis data in water_rights_scripts/fetched_data by year
#

import os
import pandas as pd
import csv
import numpy as np
import math

# make list of years
years = [str(i) for i in range(1900,2020)]
# years = years[:1]

# loop through all fetched_data
path = '../water_right_scripts/fetched_data'
users_list = os.listdir(path)
users_list.sort()
users_list.remove('.DS_Store')  # removes .DS store file name
# users_list = users_list[:100] ### restrict to first 100 users
print(users_list)

col_list = ['analysisDate', 'analysisWdid', 'analysisStructureName', 'analysisOutOfPriorityPercentOfDay',
            'priorityWdid', 'priorityStructure']

# loop through each year
for year in years:
    print(year)
    appended_data = []
    # loop through all users
    for user in users_list:
        # print(user)
        user_info = pd.read_csv(path + '/' + user, dtype=object, error_bad_lines=False, usecols=col_list)

        # extract all rows corresponding to that year
        new_df = user_info[user_info['analysisDate'].str.contains(year)]


        # drop all rows where nobody put another out of priority
        new_df = new_df.loc[new_df['priorityWdid'].notnull()]

        appended_data.append(new_df)


    appended_data = pd.concat(appended_data)
    # print(appended_data)
    appended_data.to_csv('yearly_data/' + year + '.csv', index = False)

#######################################################################
#
# '''Collect monthly data'''
# # make list of years in 21st century
# yr = '2003'
# months = [yr+'-0'+str(i)  for i in range(1,10)] + [yr+'-'+str(i) for i in range(10,13)]
# # years = years[:1]
#
# # loop through all fetched_data
# path = 'yearly_data_lite/'
#
# df = pd.read_csv(path + yr + '.csv', dtype=object, error_bad_lines=False)
#
# for m in months:
#     print(m)
#     new_df = df[df['analysisDate'].str.contains(m)]
#     print(new_df.head())
#     new_df.to_csv('monthly_data/'+ m + '.csv')







