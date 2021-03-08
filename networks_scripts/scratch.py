import os
import pandas as pd
import csv
import numpy as np
import math

# loop through all years
path = 'yearly_data/'
years = os.listdir(path)

years = ['2000.csv']

for year in years:
    df = pd.read_csv(path + year, dtype=object, error_bad_lines=False)
    print(df.columns)
    df = df.drop(['Unnamed: 0'], axis = 1)
    print(df.columns)
    df.columns = [str(x) for x in df.columns]
    print(df.columns)






#
# # obtain volume of water used by each user/node
# water_rights = pd.read_csv('../data/CDSS_WaterRights.csv', dtype=object, error_bad_lines=False)
# all_vol = water_rights[['WDID', 'Net Absolute']]
#
# for year in years:
#     df = pd.read_csv(path + year, dtype=object, error_bad_lines=False)
#     print(df.columns)
#     wdids = df.loc[['analysisWdid']]
#     print(wdids)
#     vols = []
#     for wdid in wdids:
#         vol = all_vol.loc[all_vol['WDID'] == wdid]
#
#         print(vol)








