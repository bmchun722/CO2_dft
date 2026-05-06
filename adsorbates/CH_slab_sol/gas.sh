#!/bin/bash
    mkdir gas
    cp gas_ad.py potcar_generator.sh KPOINTS mpirun_vasp.6.4.1.sh vdw_kernel.bindat INCAR ./gas/
    cp ontop/POSCAR_ontop gas/
    cd gas
    python gas_ad.py POSCAR_ontop POSCAR 2
    ./potcar_generator.sh
    echo "KPOINTS for VASPsol
0
Gamma
1 1 1
0 0 0" > KPOINTS ## > means override
    qsub mpirun_vasp.6.4.1.sh
    cd ..





