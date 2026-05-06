#!/usr/bin/bash

pbespath=/home01/x3283a08/main/bmchun/potpaw_PBE
#ldapspath=/opt/vasp/vasp_pseudopotentials/LDA
#gwpbepspath=/home/users/seungchang/software/vasppp/PBE_GW
#gwldapspath=/home/users/seungchang/software/vasppp/LDA_GW

#if [[ "$1" == lda ]]
#then
#    for i in `head -6 POSCAR | tail -1`; do
#        cat $ldapspath/$i/POTCAR >> POTCAR_temp ;
#    done
#    mv POTCAR_temp POTCAR
#elif [[ "$1" == ldagw ]]
#then
#    for i in `head -6 POSCAR | tail -1`; do
#        cat $gwldapspath/$i/POTCAR >> POTCAR_temp ;
#    done
#    mv POTCAR_temp POTCAR
#elif [[ "$1" == gw ]]
#then
#    for i in `head -6 POSCAR | tail -1`; do
#        cat $gwpbepspath/$i/POTCAR >> POTCAR_temp ;
#    done
#    mv POTCAR_temp POTCAR
#elif [[ "$1" == sv ]]
#then
    for i in `head -6 POSCAR | tail -1`; do
        echo "DEBUG: looking for path: ${pbespath}/${i}/POTCAR"
        cat /home01/x3283a08/main/bmchun/potpaw_PBE/${i}/POTCAR >> POTCAR_temp ;
    done
    mv POTCAR_temp POTCAR
#else
#    for i in `head -6 POSCAR | tail -1`; do
#        cat $pbepspath/$i/POTCAR >> POTCAR_temp ;
#    done
#    mv POTCAR_temp POTCAR
#fi


