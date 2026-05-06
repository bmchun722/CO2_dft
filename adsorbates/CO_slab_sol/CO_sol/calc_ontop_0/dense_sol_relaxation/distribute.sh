#!/bin/sh
a=-20
for i in m20 neutral p20
do 
    mkdir ${i}
    cp CONTCAR ./${i}/POSCAR
    cp POTCAR KPOINTS mpirun_vasp.6.4.1.sh vdw_kernel.bindat INCAR ./${i}/
    nelect_val=$(python get_nelect.py $((a)))
    cd ${i}
    echo "" >> INCAR
    echo "NELECT = $nelect_val" >> INCAR
    qsub mpirun_vasp.6.4.1.sh
    a=$((a+20))
    cd ..
done







