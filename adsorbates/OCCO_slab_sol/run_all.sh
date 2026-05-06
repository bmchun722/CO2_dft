#!/bin/sh

for i in bridge ontop hollow
do
    cp INCAR KPOINTS vdw_kernel.bindat potcar_generator.sh mpirun_vasp.6.4.1.sh ./${i}/
    cd ${i}
    #python symmetric.py POSCAR POSCAR 4
    ./potcar_generator.sh
    qsub mpirun_vasp.6.4.1.sh
    cd ..
done
