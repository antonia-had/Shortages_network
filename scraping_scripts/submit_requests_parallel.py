from mpi4py import MPI
import math
import os
import pandas as pd

rights = pd.read_csv('../data/CDSS_WaterRights.csv', dtype='str')
try:
    f = open('next_right', 'r')
    next_right = f.read()
    first_index = int(next_right.split()[0])
except:
    first_index = 0
rights_to_request=[]
wdids = []
dates = []
total_lines = 0
for index, row in rights.iloc[first_index:].iterrows():
    total_lines+=int(row['Lines'])
    if total_lines<2000:
        rights_to_request.append(row['Priority Admin No'])
        wdids.append(row['WDID'])
        dates.append(row['Adjudication Date'])
    else:
        with open('next_right','w') as f:
            f.write(str(index)+' '+row['Priority Admin No'])
        break

rights_no=len(rights_to_request)
print(rights_to_request)

# =============================================================================
# Start parallelization
# =============================================================================

# Begin parallel simulation
comm = MPI.COMM_WORLD

# Get the number of processors and the rank of processors
rank = comm.rank
nprocs = comm.size
print(nprocs)

# Determine the chunk which each processor will need to do
count = int(math.floor(rights_no / nprocs))
remainder = rights_no % nprocs

# Use the processor rank to determine the chunk of work each processor will do
if rank < remainder:
    start = rank * (count + 1)
    stop = start + count + 1
else:
    start = remainder * (count + 1) + (rank - remainder) * count
    stop = start + count

# =============================================================================
# Go though all rights for each processor
# =============================================================================
for k in range(start, stop):
    adminNo = rights_to_request[k]
    print(adminNo)
    WDID = wdids[k]
    startdate = dates[k]
    os.system("python3 url_request.py --adminNo {} --WDID {} --format csv --endDate 09/30/2019 "
              "--startDate {} --apiKey dBTnllEokTHF4+NOiEopD0e3MDFLP7vH --output {}.csv".format(adminNo,WDID,startdate,adminNo))
