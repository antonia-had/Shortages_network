import os
import pandas as pd

'''Identify rights to request so limit is not exceeded'''
# get list of rights already downloaded
fetched_dir = os.listdir('./fetched_data')
fetched_admins = [x[:-4] for x in fetched_dir] #gets rid of ".csv" from filename
rights = pd.read_csv('../data/CDSS_WaterRights.csv', dtype='str')
#Flip table so local user starts going through rights the other way
rights=rights.reindex(index=rights.index[::-1])
rights_to_request = []
wdids = []
dates = []
total_lines = 0
for index, row in rights.iloc[0:].iterrows():
    if not row['Priority Admin No'] in fetched_admins:
        total_lines += int(row['Lines'])
        if total_lines < 600000:
            rights_to_request.append(row['Priority Admin No'])
            wdids.append(row['WDID'])
            dates.append(row['Adjudication Date'])
        else:
            break

for k in range(len(rights_to_request)):
    adminNo = rights_to_request[k]
    WDID = wdids[k]
    startdate = dates[k]
    os.system("python3 url_request.py --adminNo {} --WDID {} --format csv --endDate 09/30/2019 "
              "--startDate {} --output {}.csv".format(adminNo, WDID, startdate, adminNo))

