#!/bin/bash
for dir in *_slab_sol; do
    cd "$dir/ontop"
    qsub mpirun_vasp.6.4.1.sh
    cd ..
    cd gas
    qsub mpirun_vasp.6.4.1.sh
    cd ../..
done

