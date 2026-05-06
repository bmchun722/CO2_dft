#!/bin/sh

for i in bridge ontop hollow
do
    cp potcar_generator.sh symmetric.py mpirun_vasp.6.4.1.sh ./${i}/
    cd ${i}
    python symmetric.py POSCAR POSCAR 2
    ./potcar_generator.sh
    qsub mpirun_vasp.6.4.1.sh
    cd ..
done
