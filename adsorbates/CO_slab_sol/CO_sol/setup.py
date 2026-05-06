import os
import shutil
import glob

# --- Configuration ---
# 1. List of files that need to go into EVERY folder
common_files = ["INCAR", "KPOINTS", "POTCAR", "mpirun_vasp.6.4.1.sh", "vdw_kernel.bindat"]

# 2. Find all your generated symmetric POSCARs
poscar_files = glob.glob("POSCAR_*_symmetric.vasp")
poscar_files.sort()

print(f"Found {len(poscar_files)} structures to set up.")

# --- Execution ---
for p_file in poscar_files:
    # 1. Generate a clean Folder Name
    # Example: "POSCAR_bridge_0_symmetric.vasp" -> "calc_bridge_0"
    folder_name = p_file.replace("POSCAR_", "calc_").replace("_symmetric.vasp", "")
    
    # 2. Create the folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # 3. Copy the Common Files (INCAR, POTCAR, KPOINTS, Script)
    for f in common_files:
        if os.path.exists(f):
            shutil.copy(f, os.path.join(folder_name, f))
        else:
            print(f"Warning: {f} missing!")
            
    # 4. Copy and Rename the POSCAR
    # VASP always looks for a file named exactly "POSCAR"
    destination_poscar = os.path.join(folder_name, "POSCAR")
    shutil.copy(p_file, destination_poscar)
    
    print(f"  [OK] Setup directory: {folder_name}")

print("\nDone. You can now submit your jobs.")
