# extract info about passives
# only works if a.list is EdgeCortix

import os
import ast

# constants
ecpn_col = 0  # a.list column with ECPN
refdescol = {'EdgeCortix': 2, 'Aetina': 6,}
desc_col = {'EdgeCortix': 5, 'Aetina': 3,}
ecpl = {
    'EC-0002C': ['0.1UF',   '16V',    'X7R',     '0201', 'CAP', 'CER'],
    'EC-0004C': ['22UF',    '6.3V',   'X5R',     '0603', 'CAP', 'CER'],
    'EC-0005C': ['10UF',    '6.3V',   'X5R',     '0402', 'CAP', 'CER'],
    'EC-0007C': ['xxxx',    'xxxx',   'xxx',     'xxxx', 'CAP', 'CER'],
    'EC-0008C': ['0.22UF',  '6.3V',   'X6S',     '0201', 'CAP', 'CER'],
    'EC-0010C': ['47PF',    '50V',    'C0G/NP0', '0201', 'CAP', 'CER'],
    'EC-0011C': ['10000PF', '10V',    'X7R',     '0201', 'CAP', 'CER'],
    'EC-0014C': ['2.2UF',   '6.3V',   'X5R',     '0201', 'CAP', 'CER'],
    'EC-0020C': ['2200PF',  '10V',    'X7R',     '0201', 'CAP', 'CER'],
    'EC-0021C': ['10PF',    'xxxx',   'xxx',  'xxxx', 'CAP', 'CER'],
    'EC-0023C': ['120PF',   'xxxx',   'xxx',  'xxxx', 'CAP', 'CER'],
    'EC-0025C': ['3300PF',  'xxxx',   'xxx',  'xxxx', 'CAP', 'CER'],
    'EC-0026C': ['6800PF',  'xxxx',   'xxx',  'xxxx', 'CAP', 'CER'],
    'EC-0027C': ['47UF',    'xxxx',   'xxx',  'xxxx', 'CAP', 'CER'],
    }
"""
EC-0004C C1          CAP CER 22UF 6.3V X5R 0603               | ----- | ['22UF', '6.3V', 'X5R', '0603', 'CAP', 'CER']
EC-0008C C2          CAP CER 0.22UF 6.3V X6S 0201             | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0002C C13         CAP CER 0.1UF 16V X7R 0201               | ----- | ['0.1UF', '16V', 'X7R', '0201', 'CAP', 'CER']
EC-0005C C23         CAP CER 10UF 6.3V X5R 0402               | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0010C C40         CAP CER                | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0011C C52         CAP CER                 | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0007C C76         CAP CER 47UF 2.5V X6S 0603               | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0023C C478        CAP CER 120PF 50V C0G/NP0 0201           | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0027C C479        CAP CER 47UF 6.3V X5R 0805               | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0021C C489        CAP CER 10PF 25V C0G/NP0 0201            | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0026C C490        CAP CER 6800PF 10V X7R 0201              | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0020C C511        CAP CER                  | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0025C C518        CAP CER 3300PF 10V X7R 0201              | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0014C C526        CAP CER                  | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
EC-0011C C533 (DNP)  CAP CER 10000PF 10V X7R 0201             | ERROR | ['xxxx', 'xxxx', 'xxx', 'xxxx', 'CAP', 'CER']
"""
def check(list, string):
    for i in list:
        if i not in string:
            return 'ERROR'
    return '-----'
# End

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

with open('temp.log', 'w') as f:
    f.write('\n')
for refdes in info[filenames[0]]:
    this_info = info[filenames[0]][refdes]
    log = this_info[0] + ' ' + refdes.ljust(12) + this_info[1].ljust(40) + ' | ' + check(this_info[2], this_info[1]) + ' | ' + str(this_info[2])
    print(log)
    with open('temp.log', 'a') as f:
        f.write(log + '\n')
# EOF
