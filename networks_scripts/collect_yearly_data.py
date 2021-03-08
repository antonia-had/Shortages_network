# sorts all structure call analysis data in water_rights_scripts/fetched_data by year
# focuses on 21st century (2000-2020)

import os
import pandas as pd
import csv
import numpy as np
import math

# make list of years in 21st century
years = [str(i) for i in range(2000,2021)]
# years = years[:1]

# loop through all fetched_data
path = '../water_right_scripts/fetched_data'
users_list = os.listdir(path)
users_list.sort()
users_list = users_list[1:]  # removes .DS store file name
# users_list = users_list[:5]
print(users_list)

# loop through each month
for year in years:
    print(year)
    appended_data = []
    # loop through all users
    for user in users_list:
        print(user)
        # extract all rows corresponding to that month in the 21st century
        user_info = pd.read_csv(path + '/' + user, dtype=object, error_bad_lines=False)
        new_df = user_info[user_info['analysisDate'].str.contains(year)]
        appended_data.append(new_df)

    appended_data = pd.concat(appended_data)
    appended_data.to_csv('yearly_data/' + year + '.csv')







