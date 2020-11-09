# Collecting data on ALL division 5 gauges
import os
import pandas as pd
import requests

'''Identify gauges to request so limit is not exceeded'''
# get list of gauges already downloaded
fetched_dir = os.listdir('./fetched_hydro_data')
fetched_gauges = [x[:-4] for x in fetched_dir] #gets rid of ".csv" from filename
gauges = pd.read_csv('../data/CDSS_streamflow_gauges_test.csv', dtype='str')
#Flip table so local user starts going through rights the other way
gauges=gauges.reindex(index=gauges.index[::-1])
gauges_to_request = []

total_lines = 0
for index, row in gauges.iloc[0:].iterrows():
    if not row['stationNum'] in fetched_gauges:
        total_lines += int(row['lines'])
        if total_lines < 1000000:
            gauges_to_request.append(row['stationNum'])
        else:
            break

for k in range(len(gauges_to_request)):
    stationNum = gauges_to_request[k]
    parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "max-measDate": '10/31/2020', "stationNum": stationNum}
    response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/surfacewater/surfacewatertsday/",
                            params=parameters)
    url_content = response.content
    filename = "/Users/ananyagangadhar/Desktop/M.Eng Project/Shortages_network/hydro_data_scripts/fetched_hydro_data/" + stationNum + ".csv"
    csv_file = open(filename, 'wb')
    csv_file.write(url_content)
    csv_file.close()