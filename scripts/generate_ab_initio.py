import sys
sys.path.append('./scripts/')
from charge_analysis import get_energy, analyze_charge_dependence
from pathlib import Path
import pandas as pd

root = Path(".")

results = []
for sp_dir in root.glob("*_gas"):
    energy = get_energy(sp_dir)
    results.append({
        "species": sp_dir.name,
        "abinitio_Energy" : energy,
        })

for sp_dir in root.glob("OCCO_slab_sol"):
    energy = get_energy(sp_dir/'ontop_30_real_fix/dense_sol/neutral/')
    results.append({
        "species": sp_dir.name,
        "abinitio_Energy" : energy,
        })


for sp_dir in root.glob("*_slab_sol"):
    energy = get_energy(sp_dir/'ontop_30_real/dense_sol/neutral/')
    results.append({
        "species": sp_dir.name,
        "abinitio_Energy" : energy,
        })


   
if results:
    df = pd.DataFrame(results)
    df.to_csv("abinitio_energies.csv", index=False)
    print(df.to_markdown(index=False))
else:
    print("something wrong")

