# Collecting data on ALL division 5 gauges
import os
import pandas as pd
import requests
import math
from csv import writer

# make a list of different kinds of climate gauges for which data is available
gauge_types = ["Evap", "FrostDate", "MaxTemp", "MinTemp", "MeanTemp", "Precip", "Snow", "SnowDepth", \
               "SnowSWE", "Solar", "VP", "Wind"]

#code collects data for each gauge type  and stores data in the respective directory
total_lines = 0
for type in gauge_types:
    '''Identify gauges to request so limit is not exceeded'''
    # get list of gauges already downloaded
    fetched_dir = os.listdir('./fetched_climate_data/' + type)
    fetched_gauges = [x[:-4] for x in fetched_dir]  # gets rid of ".csv" from filename
    gauges = pd.read_csv('../data/CDSS_climate_stations_test.csv', dtype='str')  # test dataset
    gauges = gauges.loc[gauges["measType"] == type]  #dataset with one type of climate stations

    # Flip table so local user starts going through rights the other way
    gauges = gauges.reindex(index=gauges.index[::-1])
    gauges_to_request = []


    for index, row in gauges.iloc[0:].iterrows():
        if not row['stationNum'] in fetched_gauges:
            total_lines += int(row['lines'])
            if total_lines < 1000000:
                gauges_to_request.append(row['stationNum'])
            else:
                break

    # generate API requests
    for k in range(len(gauges_to_request)):
        stationNum = gauges_to_request[k]
        parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "max-measDate": '10/31/2020',
                      "stationNum": stationNum, "measType": type}
        response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/climatedata/climatestationtsday/",
                                params=parameters)
        url_content = response.content
        filename = "/Users/ananyagangadhar/Desktop/M.Eng Project/Shortages_network/climate_data_scripts/fetched_climate_data/" \
                   + type + "/" + stationNum + ".csv"
        csv_file = open(filename, 'wb')
        csv_file.write(url_content)
        csv_file.close()
