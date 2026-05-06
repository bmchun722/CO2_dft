import sys
from ase.io import read,write

def center_z(input_path, output_path='CONTCAR_centered'):
    atoms = read(input_path)
    atoms.center()
    atoms.wrap()
    write(output_path, atoms)

center_z('POSCAR_new')

