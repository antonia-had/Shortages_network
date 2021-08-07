# sorts all structure call analysis data in water_rights_scripts/fetched_data by year
#

import os
import pandas as pd
import csv
import numpy as np
import math

# make list of years
years = [str(i) for i in range(1900,1905)]
# years = years[:1]

# loop through all fetched_data
path = '../water_right_scripts/fetched_data'
users_list = os.listdir(path)
users_list.sort()
users_list = users_list[1:]  # removes .DS store file name
# users_list = users_list[:5]
print(users_list)

col_list = ['analysisDate', 'analysisWdid', 'analysisStructureName', 'analysisOutOfPriorityPercentOfDay',
            'priorityWdid',	'priorityStructure']

# loop through each year
for year in years:
    print(year)
    appended_data = []
    # loop through all users
    for user in users_list:
        print(user)
        user_info = pd.read_csv(path + '/' + user, dtype=object, error_bad_lines=False, usecols=col_list)
        # check first row date to see if user was active that year
        if user_info['analysisDate'].iloc[0].str.contains(year):
            # extract all rows corresponding to that year
            new_df = user_info[user_info['analysisDate'].str.contains(year)]

            # drop all rows with analysisOutOfPriorityPercentOfDay = 0
            new_df = new_df.loc[new_df.analysisOutOfPriorityPercentOfDay > 0]

            appended_data.append(new_df)

    appended_data = pd.concat(appended_data)
    appended_data.to_csv('yearly_data/' + year + '.csv')

#######################################################################