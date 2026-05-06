#!/bin/sh
#PBS -V
#PBS -N bmchun
#PBS -q normal 
#PBS -A vasp
#PBS -l select=1:ncpus=64:ompthreads=1
#PBS -l walltime=3:00:00
#PBS -e myjob.err
#PBS -M bmchun722@gmail.com
#PBS -m ae 

module purge
module load intel/18.0.3 impi/18.0.3

cd $PBS_O_WORKDIR

mpirun -np 64 /home01/x3283a08/main/bmchun/vasp.6.4.1_new/bin/vasp_std > result.log
