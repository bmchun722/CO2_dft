import sys
sys.path.append('./scripts/')
from charge_analysis import get_energy, analyze_charge_dependence
from pathlib import Path
import pandas as pd

root = Path(".")
   
fixed_list = ["OCCO_slab_sol"]
    # Calculate Slab (bare) energy reference
    # Handles directories without 'ontop' subfolders
    
results = []

slab_fix_info = analyze_charge_dependence(root/"Slab_30_fix_real", "ontop_30_real_fix")
fix_slab_energy = get_energy(root/"Slab_30_fix_real/dense_sol/neutral")

slab_info = analyze_charge_dependence(root/"Slab_30_real", "ontop_30_real")
slab_energy = get_energy(root/"Slab_30_real/dense_sol/neutral")

results.append({
            "Species": "slab_fix_211",
            "Best_Site": slab_fix_info['site'],
            "Coeff_B(q^2)": slab_fix_info['coeffs'][0],    
            "Coeff_A(q)": slab_fix_info['coeffs'][1],  
            "Abinitio_energy": fix_slab_energy 
        })

results.append({
            "Species": "slab_211",
            "Best_Site": slab_info['site'],
            "Coeff_B(q^2)": slab_info['coeffs'][0],    
            "Coeff_A(q)": slab_info['coeffs'][1],  
            "Abinitio_energy": slab_energy 
        })

for sp_dir in root.glob("*_gas"):
        energy = get_energy(sp_dir)
        results.append({
            "Species": sp_dir.name,
            "Abinitio_energy" : energy
            })

        # Iterate through each species folder ending in '_slab_sol'
for sp_dir in root.glob("*_slab_sol"):
    if sp_dir.name in fixed_list:
        data_fix = analyze_charge_dependence(sp_dir, "ontop_30_real_fix")
        data_fix_energy = get_energy(sp_dir/"ontop_30_real_fix/dense_sol/neutral")
        ads_coeffs = (data_fix["coeffs"] - slab_fix_info["coeffs"]) / 2.0
        results.append({
            "Species": sp_dir.name,
            "Best_Site": data_fix['site'],
            "Coeff_B(q^2)": ads_coeffs[0],    
            "Coeff_A(q)": ads_coeffs[1],  
            "Abinitio_energy": data_fix_energy 
        })

    else:
        data = analyze_charge_dependence(sp_dir, "ontop_30_real")
        data_energy = get_energy(sp_dir/"ontop_30_real/dense_sol/neutral")
        if data is not None and slab_info is not None:
            # Calculate coefficients: (Ad_Slab_coeffs - Slab_coeffs) / 2.0
            # No gas energy subtraction included here.
            ads_coeffs = (data['coeffs'] - slab_info['coeffs']) / 2.0
            # Mapping:
            # Coeff_A = Linear term (q)
            # Coeff_B = Quadratic term (q^2)
            # Coeff_C = Constant term
            results.append({
            "Species": sp_dir.name,
            "Best_Site": data['site'],
            "Coeff_B(q^2)": ads_coeffs[0],    
            "Coeff_A(q)": ads_coeffs[1],  
            "Abinitio_energy": data_energy 
        })

            print(f"{sp_dir.name:<20} | Success | Site: {data['site']}")
        else:
            missing = "Slab" if slab_info is None else "adsorbate"
            print(f"{sp_dir.name:<20} | Skipped | Missing {missing} data (OUTCARs)")
        # Display and save results
if results:
    df = pd.DataFrame(results)
    print("\n--- Charge Dependence Analysis Results (No Gas Subtraction) ---")
    print(df.to_string(index=False))
    df.to_csv("charge_analysis_results.csv", index=False)
    print(df.to_markdown(index=False))
else:
    print("No species data found matching the criteria.")
