import pandas as pd
from datetime import datetime
import time

#extract operational life of streamflow gauges and climate stations and write into csv files

gauges = pd.read_csv("../data/CDSS_climate_stations.csv") #streamflow


min_start = datetime.strptime('1893', '%Y') #earliest start date = 01/1893
max_end = datetime.strptime('2020', '%Y') #latest end date = 10/2020

#make columns of csv file
num_indices = (max_end.year - min_start.year)
print(num_indices)
cols = [num for num in range(0,num_indices)]
cols = ['stationNum'] + cols

#make dataframe
gauges_life = pd.DataFrame(columns=cols)
print(gauges_life.head())

#iterate through rows
for i in range(len(gauges)):
    row = [gauges['stationNum'][i]]
    start_date = gauges['startDate_mod'][i]
    start_year = int(start_date.split("-")[0])
    # start_month = int(start_date.split("-")[1])
    start_ind = (start_year - 1893)

    end_date = gauges['endDate_mod'][i]
    end_year = int(end_date.split("-")[0])
    # end_month = int(end_date.split("-")[1])
    end_ind = (end_year - 1893)

    is_active = [0 for ind in range(num_indices)]
    for i in range(len(is_active)):
        if i >= start_ind and i <= end_ind:
            is_active[i] = 1
    row += is_active

    d = {}
    for i in range(len(row)):
        d[cols[i]] = row[i]

    gauges_life = gauges_life.append(d, ignore_index=True)
    # print(gauges_life.head())
    # time.sleep(1)

gauges_life.to_csv(r'../data/stations_life_yrs.csv', index = False)



