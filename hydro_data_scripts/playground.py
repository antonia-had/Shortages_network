#
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# div5_stations = pd.read_csv('../data/div5_gauges.csv', skiprows=2)
# current_stations = pd.read_csv('../data/CDSS_CurrentConditions.csv')
# count = 0
# for i in range(0,len(current_stations['USGS ID'])):
#     print(div5_stations['usgsSiteId'].str.contains(current_stations['USGS ID'][i]))
#
#
#
# print(count)
# #result = [1 for ele in current_stations['USGS ID'][:] if ele in div5_stations['usgsSiteId'][:]]
#
# #print(current_stations['USGS ID'].head())
# #print(div5_stations['usgsSiteId'].head())
# print(div5_stations['usgsSiteId'].str.contains(current_stations['USGS ID'][3])[152])
# #print(current_stations['USGS ID'][3] in div5_stations['usgsSiteId'])
# #print(current_stations['USGS ID'][3])
# #print(div5_stations['usgsSiteId'][152])
# #print(type(current_stations['USGS ID']))

print("Woohoo this works. I feel like the king of the world!!!")