
from ase.io import read
from copy import deepcopy
import sys

ads_num = int(sys.argv[3])

a = read(sys.argv[1])


a = a[a.positions[:, -1].argsort()] ## z-axis component sorting

new_a = a[-ads_num:] ## except adsorbate coords

new_a = new_a[new_a.numbers.argsort()] ## to be matched with POTCAR

new_a.set_cell([10.0,10.0,10.0])

new_a.center()

new_a.wrap()

new_a.write(sys.argv[2])
