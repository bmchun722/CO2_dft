#!/bin/bash
    mkdir dense_sol
    cp CONTCAR ./dense_sol/POSCAR
    cp POTCAR KPOINTS mpirun_vasp.6.4.1.sh vdw_kernel.bindat INCAR ./dense_sol/
    cd dense_sol
    echo "" >> INCAR ## >> append
    echo "##--VASPsol--##
LSOL = .TRUE.
EB_K = 78.4
LAMBDA_D_K = 3.0
TAU = 0" >> INCAR
    sed -i 's/EDIFF\s*=\s*1E-04/EDIFF = 1E-05/g' INCAR ## EDIFF = 1E-04 parsing
    echo "KPOINTS for VASPsol
0
Gamma
4 6 1
0 0 0" > KPOINTS ## > means override
    qsub mpirun_vasp.6.4.1.sh
    cd ..





