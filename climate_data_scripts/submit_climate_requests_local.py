# Collecting data on ALL division 5 gauges
import os
import pandas as pd
import requests
import math
from csv import writer

'''Identify gauges to request so limit is not exceeded'''
# get list of gauges already downloaded
fetched_dir = os.listdir('./fetched_climate_data')
fetched_gauges = [x[:-4] for x in fetched_dir] #gets rid of ".csv" from filename
gauges = pd.read_csv('../data/CDSS_climate_stations_test.csv', dtype='str') #test dataset
#Flip table so local user starts going through rights the other way
gauges=gauges.reindex(index=gauges.index[::-1])
gauges_to_request = []
num_pages = []

total_lines = 0
for index, row in gauges.iloc[0:].iterrows():
    if not row['stationNum'] in fetched_gauges:
        total_lines += int(row['lines'])
        if total_lines < 1000000:
            gauges_to_request.append(row['stationNum'])
            num_pages.append(math.ceil(total_lines/50000)) #number of pages the query will take
        else:
            break


for k in range(len(gauges_to_request)):
    stationNum = gauges_to_request[k]
    parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "stationNum": stationNum}
    response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/climatedata/climatestationtsday/",
                                params=parameters)
    url_content = response.content
    filename = "/Users/ananyagangadhar/Desktop/M.Eng Project/Shortages_network/climate_data_scripts/fetched_climate_data/" + stationNum + ".csv"
    csv_file = open(filename, 'wb')
    csv_file.write(url_content)
    csv_file.close()

    if num_pages[k] > 1: #create multiple requests for same stationNum if query takes more than one page
        for l in range(2,num_pages[k]+1):
            parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "stationNum": stationNum,
                          "pageIndex": str(l)}
            response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/climatedata/climatestationtsday/",
                                    params=parameters)
            url_content = response.content
            filename2 = "/Users/ananyagangadhar/Desktop/M.Eng Project/Shortages_network/data/junk.csv"
            csv_file2 = open(filename2, 'wb')
            csv_file2.write(url_content)
            csv_file2.close()

            #combine both csv files
            a = pd.read_csv(filename, header=2)
            b = pd.read_csv(filename2, header=2)
            combo = a.append(b, ignore_index=True)
            combo.to_csv(filename, index=False)
    else:
        a = pd.read_csv(filename, header=2)
        a.to_csv(filename, index=False)


