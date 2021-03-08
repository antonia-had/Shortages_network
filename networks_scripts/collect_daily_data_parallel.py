from mpi4py import MPI
import os
import pandas as pd

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#################################################################################################################
def day_water_rights(date = '2002-09-09'):
    # returns .csv file showing all calls for a particular day
    # format date as YYYY-MM-DD string


    path = 'yearly_data/'
    years_list = os.listdir(path)
    years_list = years_list[1:] # removes .DS store file name

    for year in years_list:
       if date[:4] == year[:-4]:
           df = pd.read_csv(path + year, dtype=object, error_bad_lines=False)
           df = df.drop(df.columns[0], axis=1)
           new_df = df[df['analysisDate'].str.contains(date)]
           new_df.to_csv('daily_data_v2/' + date + '.csv')
           break

#################################################################################################################


'''Master to determine number of tasks for the day and divide among cores'''
if rank == 0:

    # divide all dates
    dates = dates = pd.date_range(start="2000-01-01", end="2020-10-31")
    dates = [i.strftime('%Y-%m-%d') for i in dates]

    # determine the size of each sub-task
    ave, res = divmod(len(dates), size)
    counts = [ave + 1 if p < res else ave for p in range(size)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(size)]
    ends = [sum(counts[:p + 1]) for p in range(size)]

    # converts data into a list of arrays
    dates_to_request = [dates[starts[p]:ends[p]] for p in range(size)]

else:
    dates_to_request = None

'''Scatter tasks from master to every core'''
dates_to_request = comm.scatter(dates_to_request, root=0)


'''Every core goes through its assigned tasks'''
print('Process {} has to retrieve rights:'.format(rank), dates_to_request)
for k in range(len(dates_to_request)):
    day_water_rights(k)