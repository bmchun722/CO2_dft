from ase.io import read
import numpy as np
import os
from pathlib import Path


Slab_path = Path('Slab')
ad_slab_path = Path('ontop')
output_Slab = Slab_path / 'dense_sol/neutral/vasprun.xml'
output_ad_slab = ad_slab_path / 'dense_sol/neutral/vasprun.xml'
#for p in Path.cwd().rglob('OUTCAR'):
#    print(p)

out_slab = read(output_Slab, index='-1')
out_ad_slab = read(output_ad_slab, index='-1')


slab_toten = out_slab.get_potential_energy()
out_ad_toten = out_ad_slab.get_potential_energy()

adsorption_e = 0.5*(out_ad_toten - slab_toten)

print(adsorption_e)
## choose smaller adsorption_e 


charge = [ 'm20' ,'m10' , 'neutral' ,'p10', 'p20']
slab_totens = []
for i in charge:
    
    out_slabs = read(Slab_path/f'dense_sol/{i}/vasprun.xml', index='-1')
    out_slabs_toten = out_slabs.get_potential_energy()
    slab_totens.append(out_slabs_toten)

a = np.polyfit([-20,-10,0,10,20] , slab_totens, 2)


ad_slab_totens = []
for i in charge:
    
    out_ad_slabs = read(ad_slab_path/f'dense_sol/{i}/vasprun.xml', index='-1')
    out_ad_slabs_toten = out_ad_slabs.get_potential_energy()
    ad_slab_totens.append(out_ad_slabs_toten)

b = np.polyfit([-20,-10,0,10,20] , ad_slab_totens, 2)

exact_data_points = []

for i in range(len(charge)):
    exact = 0.5*(ad_slab_totens[i]- slab_totens[i])
    exact_data_points.append(exact)
print(exact_data_points)


coeffs = b - a

coeffs[-1] = coeffs[-1]

coeffs = coeffs / 2.0

print(coeffs)


import matplotlib.pyplot as plt 

x_fit = np.linspace(-30, 30, 100)
y_fit = np.polyval(coeffs, x_fit)

plt.plot(x_fit, y_fit, label='Fit Model_OCCO_(211)')
plt.scatter([-20,-10,0,10,20], exact_data_points)
plt.legend()
plt.ylabel("Adsorption Energy(eV)")       
plt.show()


