from pymatgen.core import Structure
import sys
import numpy as np ## for calculating area
from scipy import constants  ## for unit conversion

struct = Structure.from_file("POSCAR")


valence_electrons = {"Cu" : 11, "C" : 4 , "O" : 6, "H" : 1}
nelect = sum(valence_electrons[specie.symbol] * count for specie, count in struct.composition.items())

matrix = struct.lattice.matrix
area = np.linalg.norm(np.cross(matrix[0],matrix[1]))
total_area = 2.0 * area ## symmetry slab
e = constants.e
angstrom_to_cm = constants.angstrom / constants.centi
coulomb_to_micro = 1 / constants.micro

unit_conversion = e / (angstrom_to_cm ** 2) * coulomb_to_micro
delta_n = -1 * float(sys.argv[1]) * total_area / unit_conversion
nelect += delta_n
print(nelect)
