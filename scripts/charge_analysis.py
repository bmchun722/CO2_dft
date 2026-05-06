import numpy as np
from ase.io.vasp import read_vasp_out
from ase.io import read,write 
from pathlib import Path
import pandas as pd

def get_energy(path):
    """Helper function to read potential energy from VASP output files."""
    xml_file = path / 'vasprun.xml'
    out_file = path / 'OUTCAR' 
    
    if xml_file.exists():
        atoms = read(str(xml_file), index=-1, format='vasp-xml')
        return atoms.get_potential_energy()


    if out_file.exists():
        atoms = read_vasp_out(str(out_file))
        return atoms.get_potential_energy()

def analyze_charge_dependence(species_path, directory_for_calc):
    """
    Finds the most stable site (if available) and performs charge fitting.
    Handles both 'ontop' sub-directories and direct 'dense_sol' structures.
    """
    # 1. Identify the base directory for calculations
    site_dirs = list(species_path.glob(directory_for_calc))
    print(site_dirs)
    
    if not site_dirs:
        # Case: Slab_relax (no ontop folders, dense_sol is directly here)
        best_site_path = species_path
        site_label = species_path.name
    else:
        # Case: Adsorbate species (find the best ontop site based on 'neutral')
        best_site_path = None
        site_label = None
        min_neutral_e = float('inf')

        for site in site_dirs:
            neutral_e = get_energy(site / "dense_sol/neutral")
            if neutral_e < min_neutral_e:
                min_neutral_e = neutral_e
                best_site_path = site
                site_label = site.name

    if not best_site_path:
        return None

    # 2. Collect energies for each charge state
    # Using integer scale as requested
    q_values = [-20, -10, 0, 10, 20] 
    q_folders = ['m20', 'm10', 'neutral', 'p10', 'p20']
    
    y_energies = []
    for q_dir in q_folders:
        e = get_energy(best_site_path / "dense_sol" / q_dir)
        if e is None: 
            return None # Skip if any charge state is missing
        y_energies.append(e)

    # 3. Polynomial fit (2nd order)
    # coeffs[0] = quadratic (q^2), coeffs[1] = linear (q), coeffs[2] = constant
    coeffs = np.polyfit(q_values, y_energies, 2)
    return {"site": site_label, "coeffs": coeffs, "energies": y_energies}

def center_z(input_path, output_path='CONTCAR_centered'):
    atoms = read(input_path)
    atoms.center()
    atoms.wrap()
    write(output_path, atoms)





# --- Main Execution Logic ---
#if __name__ == "__main__":
#    root = Path(".")
   
#    exclude_list = []
#    # Calculate Slab (bare) energy reference
#    # Handles directories without 'ontop' subfolders
#    
#    results = []
#        # Iterate through each species folder ending in '_slab_sol'
#    for sp_dir in root.glob("*_slab_sol"):
#        if sp_dir.name in exclude_list:
#            continue
#        slab_info = analyze_charge_dependence(root / "Slab_40_fix")
#        print(sp_dir)
#        data = analyze_charge_dependence(sp_dir)
#        if data is not None and slab_info is not None:
#            # Calculate coefficients: (Ad_Slab_coeffs - Slab_coeffs) / 2.0
#            # No gas energy subtraction included here.
#            ads_coeffs = (data['coeffs'] - slab_info['coeffs']) / 2.0
#            print(sp_dir) 
#            # Mapping:
#            # Coeff_A = Linear term (q)
#            # Coeff_B = Quadratic term (q^2)
#            # Coeff_C = Constant term
#            results.append({
#                "Species": sp_dir.name,
#                "Best_Site": data['site'],
#                "Coeff_B(q^2)": ads_coeffs[0],    
#                "Coeff_A(q)": ads_coeffs[1],  
#                "Coeff_C(const)": ads_coeffs[2] 
#            })
#
#            print(f"{sp_dir.name:<20} | Success | Site: {data['site']}")
#        else:
#            missing = "Slab" if slab_info is None else "adsorbate"
#            print(f"{sp_dir.name:<20} | Skipped | Missing {missing} data (OUTCARs)")
#        # Display and save results
#if results:
#    df = pd.DataFrame(results)
#    print("\n--- Charge Dependence Analysis Results (No Gas Subtraction) ---")
#    print(df.to_string(index=False))
#    df.to_csv("charge_analysis_results.csv", index=False)
#    print(df.to_markdown(index=False))
#else:
#    print("No species data found matching the criteria.")
