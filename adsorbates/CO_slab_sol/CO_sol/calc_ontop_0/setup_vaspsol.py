import os
import shutil

# ==========================================
# Configuration
# ==========================================
current_dir = os.getcwd()
new_subfolder = "CO_ontop_0_sol"
target_dir = os.path.join(current_dir, new_subfolder)

# Files to copy DIRECTLY (without modification)
# removed INCAR from here because we will handle it separately
files_to_copy = [
    "POTCAR", 
    "vdw_kernel.bindat", 
    "mpirun_vasp.6.4.1.sh"
]

# Lines to append to INCAR
incar_append_lines = """
! --- VASPsol Settings ---
LSOL = .TRUE.
EB_K = 78.4
LAMBDA_D_K = 3.0
TAU = 0
"""

# New KPOINTS content
new_kpoints_content = """KPOINTS for VASPsol (4 6 1)
0
Gamma
4  6  1
0  0  0
"""


# 1. Create subdirectory
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"  [Create] Directory: {new_subfolder}")
else:
    print(f"  [Info] Directory {new_subfolder} already exists.")

# 2. Copy standard files (POTCAR, Script, etc.)
for filename in files_to_copy:
    src_path = os.path.join(current_dir, filename)
    dst_path = os.path.join(target_dir, filename)
    
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"  [Copy] {filename}")
    else:
        print(f"  [Warning] {filename} not found.")

# 3. Handle INCAR (Copy + Append)
src_incar = os.path.join(current_dir, "INCAR")
dst_incar = os.path.join(target_dir, "INCAR")

if os.path.exists(src_incar):
    with open(src_incar, 'r') as f_in:
        original_content = f_in.read()
    
    # Write original content + new lines
    with open(dst_incar, 'w') as f_out:
        f_out.write(original_content)
        f_out.write("\n") # Ensure there is a newline
        f_out.write(incar_append_lines)
    
    print(f"  [Edit] INCAR copied and appended VASPsol tags.")
else:
    print(f"  [Error] INCAR not found.")

# 4. Copy CONTCAR -> POSCAR
src_contcar = os.path.join(current_dir, "CONTCAR")
dst_poscar = os.path.join(target_dir, "POSCAR")

if os.path.exists(src_contcar):
    if os.path.getsize(src_contcar) > 0:
        shutil.copy(src_contcar, dst_poscar)
        print(f"  [Copy] CONTCAR -> {new_subfolder}/POSCAR")
    else:
        print(f"  [Error] CONTCAR is empty.")
else:
    print(f"  [Error] CONTCAR not found.")

# 5. Write new KPOINTS
kpoints_path = os.path.join(target_dir, "KPOINTS")
with open(kpoints_path, "w") as f:
    f.write(new_kpoints_content)
print(f"  [Create] KPOINTS (4 6 1)")

print("Done.")
