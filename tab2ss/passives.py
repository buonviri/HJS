# extract info about passives
# only works if a.list is EdgeCortix

import os
import ast

# constants
ecpn_col = 0  # a.list column with ECPN
refdescol = {'EdgeCortix': 2, 'Aetina': 6,}
desc_col = {'EdgeCortix': 5, 'Aetina': 3,}
ecpl = {
    'EC-0002C': ['0.1UF',  '16V',  'X7R',  '0201', 'CAP', 'CER'],
    'EC-0004C': ['22UF',   '6.3V', 'X5R',  '0603', 'CAP', 'CER'],
    }

# main()
filenames = ['a.list', 'b.list']
info = {filenames[0]: {}, filenames[1]: {},}  # blank dicts
for filename in filenames:
    with open(filename, 'r') as f:
        ss = ast.literal_eval(f.read())  # convert to spreadsheet
    if ss[0][0] in ['ECPN',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'EdgeCortix'
    elif ss[0][0] in ['Model',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'Aetina'
    else:
        id = 'Invalid format'
    print('\n' + id + ': ' + str(ss[0]))
    for row in ss[1:]:  # skip header row
        refdes = row[refdescol[id]]
        desc = row[desc_col[id]]
        ecpn = ''
        if id == 'EdgeCortix':
            try:
                ecpn = ecpl[row[ecpn_col]]
            except:
                ecpn = 'Need to add ' + row[ecpn_col]
        else:
            ecpn = 'n/a'
        if refdes.startswith('C'):
            info[filename][refdes.split(',')[0]] = [row[ecpn_col], desc, ecpn]

# print(info)
# print(info[filenames[0]]['C1'])
# print(info[filenames[1]]['C1'])

for refdes in info[filenames[0]]:
    this_info = info[filenames[0]][refdes]
    print(this_info[0] + ' ' + refdes.ljust(12) + this_info[1] + ' | ' + str(this_info[2]))

# EOF
