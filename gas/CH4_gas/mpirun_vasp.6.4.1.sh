#!/bin/sh
#PBS -V
#PBS -N bmchun
#PBS -q debug 
#PBS -A vasp
#PBS -l select=1:ncpus=64:ompthreads=1
#PBS -l walltime=1:00:00
#PBS -e myjob.err
#PBS -M bmchun722@gmail.com
#PBS -m ae 

module purge
module load craype-mic-knl intel/oneapi_21.2 impi/oneapi_21.2 hdf5/1.10.2 fftw_mpi/3.3.7
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home01/x3283a08/main/bmchun/vasp.6.4.1/bin/dftd4/lib64

cd $PBS_O_WORKDIR

mpirun -np 64 /home01/x3283a08/main/bmchun/vasp.6.4.1/bin/vasp_std > result.log
