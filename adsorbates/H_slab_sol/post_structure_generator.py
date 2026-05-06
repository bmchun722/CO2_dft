from pymatgen.core import Structure, Molecule
from pymatgen.io.vasp import Poscar
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
import numpy as np

# 1. Load file
base_structure = Structure.from_file("./POSCAR_Cu211_Base")
inversion_center = np.mean(base_structure.frac_coords, axis=0) ## exact inversion fractional coordinate for slab
# 2. Define Molecule (C-O)
molecule = Molecule(["C","H"], [[0.0, 0, 0], [0.0, 0, 1.1]])

# 3. Find Sites
asf = AdsorbateSiteFinder(base_structure)
sites_dict = asf.find_adsorption_sites(distance=1.85) ## finding the adsorption sites.

if "selective_dynamics" not in base_structure.site_properties:
    num_atoms = len(base_structure)
    base_structure.add_site_property("selective_dynamics", [[True, True, True]] * num_atoms) ## make it possible to be relaxed

print("Generating SYMMETRIC labeled structures (Manual Mode)...")

for label, coords_list in sites_dict.items():
    if label == 'all': continue

    for i, top_coord in enumerate(coords_list):

        # --- A. Copy Structure ---
        struct = base_structure.copy()

        # --- B. Add [Top] Molecule ---
        mol_top = molecule.copy()
        mol_top.translate_sites(indices=range(len(mol_top)), vector=top_coord)

        for atom in mol_top:
            struct.append(
                atom.specie,
                atom.coords,
                coords_are_cartesian=True,
                properties={"selective_dynamics": [True, True, True]}
            )

        struct.sort(key=lambda s: s.specie.Z, reverse=True)

        # --- E. Save ---
        filename = f"POSCAR_{label}_{i}_symmetric.vasp"
        Poscar(struct).write_file(filename)
        print(f"Saved: {filename}")    

