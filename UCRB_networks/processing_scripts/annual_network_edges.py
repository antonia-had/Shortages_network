import pandas as pd
import os
import networkx as nx



'''Create .csv files with network edges and edge attributes'''
#
# path = 'annual_data/'
# m_list = os.listdir(path)
# m_list.sort()
# # m_list = [m_list[0]]
# print(m_list)
#
# for m in m_list:
#     print(m)
#     df = pd.read_csv(path + m)
#
#     df['analysisOutOfPriorityPercentOfDay'] = df['analysisOutOfPriorityPercentOfDay'].div(100)
#     # drop duplicate rows to ensure number of days out of priority does not exceed 365
#     new_df = df.drop_duplicates(subset=['analysisDate', 'analysisWrAdminNo', 'priorityAdminNo'],
#         keep='first').reset_index(drop=True)
#
#     # drop date row
#     new_df = new_df.drop('analysisDate', 1)
#
#     # number of days one water right (analysisWrAdminNo) was put out of priority by a specific priorityAdminNo
#     new_df = new_df.groupby(["analysisWrAdminNo", "priorityAdminNo"]).analysisOutOfPriorityPercentOfDay.agg([sum]).reset_index()
#     new_df = new_df.rename(columns={"analysisWrAdminNo": "analysisAdminNo", "sum": "wt"})
#     new_df = new_df.sort_values(by=['wt'], ascending=False)
#
#     new_df.to_csv('annual_networks/' + m, index=False)

######################################################################################################

'''Add attribute columns to network csv files'''

# analysisAdminNo  priorityAdminNo  wt*  analysisDistrict  priorityDistrict  analysisStreamMile  priorityStreamMile
# analysisNetAbs  priorityNetAbs

# add analysisDistrict analysisStreamMile analysisNetAbs to network

path = 'annual_networks/'
m_list = os.listdir(path)
m_list.sort()
print(m_list)
# m_list = [m_list[0]]

for m in m_list:
    print(m)
    df = pd.read_csv(path + m)

    attr = pd.read_csv('../data/Attributes.csv')

    # add analysisAdminNo attributes
    new_df = pd.merge(df, attr, left_on='analysisAdminNo', right_on='adminNumber')
    new_df = new_df.drop(['adminNumber', 'adjudicationDate', 'latitude', 'longitude'],1)
    new_df = new_df.rename(columns={"streamMile": "analysisStreamMile",
                                    "netAbs": "analysisNetAbs", "district": "analysisDistrict", "wdid": "analysisWdid"})
    new_df["wt"] = new_df["wt"] * new_df["analysisNetAbs"]
    new_df = new_df.loc[new_df['wt'] > 0]


    # add priorityAdminNo attributes
    new_df = pd.merge(new_df, attr, left_on='priorityAdminNo', right_on='adminNumber')
    new_df = new_df.drop(['adminNumber', 'adjudicationDate', 'latitude', 'longitude'],1)
    new_df = new_df.rename(columns={"streamMile": "priorityStreamMile",
                                    "netAbs": "priorityNetAbs", "district": "priorityDistrict", "wdid": "priorityWdid"})



    new_df.to_csv('../network_scripts/network_csv/' + m, index=False)