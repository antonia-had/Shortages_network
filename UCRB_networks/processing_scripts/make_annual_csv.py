import pandas as pd
import os
import networkx as nx

# make list of years
years = [str(i) for i in range(1988,2020)]

# loop through all fetched_data
path = '../data/fetched_data'
users_list = os.listdir(path)
users_list.sort()
users_list.remove('.DS_Store')  # removes .DS store file name
# users_list = users_list[:10] ### restrict to first 100 users
print(users_list)

col_list = ['analysisDate', 'analysisWrAdminNo', 'analysisOutOfPriorityPercentOfDay',
            'priorityAdminNo']

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
        new_df = new_df.loc[new_df['priorityAdminNo'].notnull()]
        new_df = new_df.loc[new_df['analysisOutOfPriorityPercentOfDay'] > 0]


        appended_data.append(new_df)

    appended_data = pd.concat(appended_data)
    # print(appended_data)
    appended_data.to_csv('annual_data/' + year + '.csv', index = False)