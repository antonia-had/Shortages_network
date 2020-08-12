from mpi4py import MPI
import os
import pandas as pd

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

'''Master to determine number of tasks for the day and divide among cores'''
if rank == 0:
    '''Identify rights to request so limit is not exceeded'''
    rights = pd.read_csv('../data/CDSS_WaterRights.csv', dtype='str')
    try:
        f = open('next_right', 'r')
        next_right = f.read()
        first_index = int(next_right.split()[0])
    except:
        first_index = 0
    rights_to_request = []
    wdids = []
    dates = []
    total_lines = 0
    for index, row in rights.iloc[first_index:].iterrows():
        total_lines += int(row['Lines'])
        if total_lines < 800000:
            rights_to_request.append(row['Priority Admin No'])
            wdids.append(row['WDID'])
            dates.append(row['Adjudication Date'])
        else:
            # Print placeholder right to pick up from next time
            with open('next_right', 'w') as f:
                f.write(str(index) + ' ' + row['Priority Admin No'])
            break
    '''Divide tasks to be executed by each core'''
    # determine the size of each sub-task
    ave, res = divmod(len(rights_to_request), size)
    counts = [ave + 1 if p < res else ave for p in range(size)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(size)]
    ends = [sum(counts[:p+1]) for p in range(size)]

    # converts data into a list of arrays
    rights_to_request = [rights_to_request[starts[p]:ends[p]] for p in range(size)]
    wdids = [wdids[starts[p]:ends[p]] for p in range(size)]
    dates = [dates[starts[p]:ends[p]] for p in range(size)]

else:
    rights_to_request = None
    wdids = None
    dates = None

'''Scatter tasks from master to every core'''
rights_to_request = comm.scatter(rights_to_request, root=0)
wdids = comm.scatter(wdids, root=0)
dates = comm.scatter(dates, root=0)

'''Every core goes through its assigned tasks'''
print('Process {} has to retrieve rights:'.format(rank), rights_to_request)
for k in range(len(rights_to_request)):
    adminNo = rights_to_request[k]
    WDID = wdids[k]
    startdate = dates[k]
    os.system("python3 url_request.py --adminNo {} --WDID {} --format csv --endDate 09/30/2019 "
              "--startDate {} --apiKey dBTnllEokTHF4+NOiEopD0e3MDFLP7vH --output {}.csv".format(adminNo, WDID,
                                                                                                startdate, adminNo))

