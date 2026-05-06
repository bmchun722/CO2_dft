
from ase.io import read
from copy import deepcopy
import sys

ads_num = int(sys.argv[3])

a = read(sys.argv[1])


a = a[a.positions[:, -1].argsort()] ## z-axis component sorting

top = a[-ads_num:] ## only adsorbate coords 
new_a = a[:-ads_num] ## except adsorbate coords
bot_new = deepcopy(top)
slab_center = new_a.positions.mean(axis=0)
bot_new.positions = 2*slab_center - top.positions
bot_new.wrap() ## maybe this is what makes good centering 
new_a = new_a + bot_new + top ## 

new_a = new_a[new_a.numbers.argsort()] ## to be matched with POTCAR

new_a.wrap()

new_a.write(sys.argv[2])
