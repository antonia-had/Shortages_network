#!/bin/bash
#SBATCH --job-name="CDSS_requests"
#SBATCH --output="requests.out"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --export=ALL
#SBATCH -t 0:10:00            # set max wallclock time

module load python/3.6.9
source /home/fs02/pmr82_0001/ah986/envs/shortage_network/bin/activate
mpirun -n 1 python3 submit_requests_parallel.py

