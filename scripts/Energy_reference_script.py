
from ase.symbols import string2symbols

abinitio_energies = {
        'CO2_gas': -18.421, 
        'CO_gas': -12.0935, 
        'OH_gas': -5.67174,
        'H2_gas': -7.17327, 
        'CH4_gas': -23.2902,
        'CH3CH2OH_gas': -43.3659,
        'H2O_gas': -12.8318,
        'slab_211': -19.0227,
        'H_211': -26.2173,   
        'CO_211': -44.6345, 
        'CHO_211': -50.7556, 
        'CHOH_211': -57.5807,
        'CH_211': -38.5966,
        'OCCO_211': -68.1759,
        'OCCOH_211': -74.3149,
        'CO2_211': -55.05651317,
        'COOH_211': -63.1941,
        }

ref_dict = {}
ref_dict['H'] = 0.5*abinitio_energies['H2_gas']
ref_dict['O'] = abinitio_energies['H2O_gas'] - 2*ref_dict['H']
ref_dict['C'] = abinitio_energies['CO_gas'] - ref_dict['O']
ref_dict['211'] = abinitio_energies['slab_211']

def get_formation_energies(energy_dict,ref_dict):
    formation_energies = {}
    for key in energy_dict.keys(): #iterate through keys
        E0 = energy_dict[key] #raw energy
        name,site = key.split('_') #split key into name/site
        if 'slab' not in name: #do not include empty site energy (0)
            #remove - from transition-states
            formula = name.replace('-','')
            #get the composition as a list of atomic species
            composition = string2symbols(formula)
            if site == '211':
                E0 -= ref_dict[site] #subtract slab energy if adsorbed
            #for each atomic species, subtract off the reference energy
            # 2 because when symmetric slab
            
                for atom in composition:
                    E0 -= 2*ref_dict[atom]
                    E0 = round(E0,3)
                    formation_energies[key] = E0/2
                    print(formation_energies)
            elif site == 'gas': ## gas_species
                for atom in composition:
                    E0 -= ref_dict[atom]
                    E0 = round(E0,3)
                    formation_energies[key] = E0
    return formation_energies

formation_energies = get_formation_energies(abinitio_energies,ref_dict)

for key in formation_energies:
    print(key, formation_energies[key])

frequency_dict = {
        'CO2_gas': [2.3, 5.5, 633.1, 633.7, 1347.6, 2384.0], 
        'CO_gas': [6.2, 14.3, 2157.1], 
        'OH_gas': [],
        'H2_gas': [0.3, 0.8, 4450.3], 
        'CH4_gas': [51.8, 65.8, 75.6, 1329.3, 1329.6, 1331.7, 1547.3, 1548.3, 2992.3, 3118.4, 3118.9, 3119.4],
        'CH3CH2OH_gas': [25.6,98.0,132.1,244.5,285.9,427.3,814.3,872.8,1008.4,1070.6,1159.1,1254.9,1278.5,1389.7,1424.1,1468.7,1485.8,1508.3,2953.1,2975.9,3004.9,3085.1,3087.1,3758.5],
        'H2O_gas': [211.4, 250.4, 1634.7, 3753.1, 3849.2],
        'H_211': [459.5, 563.0, 995.3],   
        'CO_211': [2040.0, 306.9, 268.2, 261.1, 99.7, 68.7], 
        'CHO_211': [2767.1, 1659.6, 1220.8, 664.3, 396.5, 221.4, 88.4, 73.2, 36.6], 
        'CHOH_211': [3656.8, 2964.2, 1378.6, 1198.8, 1018.8, 704.1, 400.0, 328.0, 216.2, 208.9, 152.2, 63.3],
        'CH_211': [379.0, 380.0, 503.1, 599.3, 599.4, 3065.5],
        'OCCO_211': [161.3,176.3,203.4,260.2,323.5,336.3,358.5,540.2,654.6,808.5,1375.4,1594.3],
        'OCCOH_211': [148.9, 196.4, 213.8, 243.5, 264.2, 316.5, 324.1, 512.9, 681.9, 775.4, 881.0, 1029.9, 1292.6, 1348.3, 3415.8],
        'CO2_211': [242.3, 246.5, 303.2, 321.1, 363.3, 748.1, 1186.6, 1443.0],
        'COOH_211': [79.1, 110.1, 221.3, 269.0, 360.9, 669.6, 711.2, 1107.9, 1272.6, 1483.8, 3496.2],
                }


def make_input_file(file_name,energy_dict,frequency_dict):

    #create a header
    header = '\t'.join(['surface_name','site_name',
                        'species_name','formation_energy',
                        'frequencies','reference'])

    lines = [] #list of lines in the output
    for key in energy_dict.keys(): #iterate through keys
        E = energy_dict[key] #raw energy
        name,site = key.split('_') #split key into name/site
        if 'slab' not in name: #do not include empty site energy (0)
            frequency = frequency_dict[key]
            if site == 'gas':
                surface = None
            else:
                surface = 'Cu'
            outline = [surface,site,name,E,frequency,'Input File Tutorial.']
            line = '\t'.join([str(w) for w in outline])
            lines.append(line)

    lines.sort() #The file is easier to read if sorted (optional)
    lines = [header] + lines #add header to top
    input_file = '\n'.join(lines) #Join the lines with a line break

    input = open(file_name,'w') #open the file name in write mode
    input.write(input_file) #write the text
    input.close() #close the file

    print('Successfully created input file')

file_name = 'energies.txt'
make_input_file(file_name,formation_energies,frequency_dict)

#Test that input is parsed correctly
from catmap.model import ReactionModel
from catmap.parsers import TableParser
rxm = ReactionModel()
#The following lines are normally assigned by the setup_file
#and are thus not usually necessary.
rxm.surface_names = ['Cu']
rxm.adsorbate_names = ('CO','C','O','H','CH','OH','CH2','CH3') 
rxm.transition_state_names = ('H2O-ele*_t','H-H2O-ele*_t','H-H*_t','CO-*_t','H2O-CO-ele*_t')
rxm.gas_names = ('CO2_g','CO_g','CH4_g','H2O_g','H2_g','CH3CH2OH_g','ele_g')
rxm.site_names = ('211')
rxm.species_definitions = {'t':{'site_names':['211']}}
#Now we initialize a parser instance (also normally done by setup_file)
parser = TableParser(rxm)
parser.input_file = file_name
parser.parse()
#All structured data is stored in species_definitions; thus we can
#check that the parsing was successful by ensuring that all the
#data in the input file was collected in this dictionary.
for key in rxm.species_definitions:
    print(key, rxm.species_definitions[key])

