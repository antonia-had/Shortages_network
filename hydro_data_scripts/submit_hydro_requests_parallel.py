from mpi4py import MPI
import os
import pandas as pd
import requests

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

'''Master to determine number of tasks for the day and divide among cores'''
if rank == 0:
    '''Identify gauges to request so limit is not exceeded'''
    # get list of gauges already downloaded
    fetched_dir = os.listdir('./fetched_hydro_data')
    fetched_gauges = [x[:-4] for x in fetched_dir]  # gets rid of ".csv" from filename
    gauges = pd.read_csv('../data/CDSS_streamflow_gauges.csv', dtype='str')
    # Flip table so local user starts going through rights the other way
    gauges = gauges.reindex(index=gauges.index[::-1])
    gauges_to_request = []

    total_lines = 0
    for index, row in gauges.iloc[0:].iterrows():
        if not row['stationNum'] in fetched_gauges:
            total_lines += int(row['lines'])
            if total_lines < 1000000:
                gauges_to_request.append(row['stationNum'])
            else:
                break

    '''Divide tasks to be executed by each core'''
    # determine the size of each sub-task
    ave, res = divmod(len(gauges_to_request), size)
    counts = [ave + 1 if p < res else ave for p in range(size)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(size)]
    ends = [sum(counts[:p+1]) for p in range(size)]

    # converts data into a list of arrays
    gauges_to_request = [gauges_to_request[starts[p]:ends[p]] for p in range(size)]


else:
    gauges_to_request = None


'''Scatter tasks from master to every core'''
gauges_to_request = comm.scatter(gauges_to_request, root=0)


'''Every core goes through its assigned tasks'''
print('Process {} has to retrieve rights:'.format(rank), gauges_to_request)
for k in range(len(gauges_to_request)):
    stationNum = gauges_to_request[k]
    parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "max-measDate": '10/31/2020', "stationNum": stationNum}
    response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/surfacewater/surfacewatertsday/",
                            params=parameters)
    url_content = response.content
    filename = "fetched_hydro_data/" + stationNum + ".csv"
    csv_file = open(filename, 'wb')
    csv_file.write(url_content)
    csv_file.close()