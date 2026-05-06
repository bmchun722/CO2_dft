#!/bin/sh
a=-20
for i in m20 m10 neutral p10 p20
do 
    mkdir ${i}
    cp CONTCAR ./${i}/POSCAR
    cp POTCAR KPOINTS mpirun_vasp.6.4.1.sh vdw_kernel.bindat INCAR ./${i}/
    nelect_val=$(python get_nelect.py $((a)))
    cd ${i}
    sed -i '/NELECT/d' INCAR
    echo "" >> INCAR
    echo "NELECT = $nelect_val" >> INCAR
    #sed -i 's/NSW\s*=\s*1000/NSW = 0/g' INCAR
    qsub mpirun_vasp.6.4.1.sh
    a=$((a+10))
    cd ..
done







