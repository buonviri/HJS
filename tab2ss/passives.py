# extract info about passives
# only works if a.list is EdgeCortix

import os
import ast

# constants
ecpn_col = 0  # a.list column with ECPN
refdescol = {'EdgeCortix': 2, 'Aetina': 6,}
desc_col = {'EdgeCortix': 5, 'Aetina': 3,}
ecpl = {
    'EC-0002C': ['0.1UF',  '16V',  'X7R',     '0201',],
    'EC-0003C': ['47UF',   '25V',  'X5R',     '1206',],
    'EC-0004C': ['22UF',   '6.3V', 'X5R',     '0603',],
    'EC-0005C': ['10UF',   '6.3V', 'X5R',     '0402',],
    'EC-0007C': ['47UF',   '2.5V', 'X6S',     '0603',],
    'EC-0008C': ['0.22UF', '6.3V', 'X6S',     '0201',],
    'EC-0009C': ['10UF',   '25V',  'X5R',     '0603',],
    'EC-0010C': ['47PF',   '50V',  'C0G/NP0', '0201',],
    'EC-0011C': ['0.01UF', '10V',  'X7R',     '0201',],  # value gets replaced
    'EC-0013C': ['1UF',    '6.3V', 'X5R',     '0201',],
    'EC-0014C': ['2.2UF',  '6.3V', 'X5R',     '0201',],
    'EC-0019C': ['100UF',   '4V',  'X6S',     '1206',],
    'EC-0020C': ['2.2NF',  '10V',  'X7R',     '0201',],  # value gets replaced
    'EC-0021C': ['10PF',   '25V',  'C0G/NP0', '0201',],
    'EC-0023C': ['120PF',  '50V',  'C0G/NP0', '0201',],
    'EC-0025C': ['3.3NF',  '10V',  'X7R',     '0201',],  # value gets replaced
    'EC-0026C': ['6800PF', '10V',  'X7R',     '0201',],
    'EC-0027C': ['47UF',   '6.3V', 'X5R',     '0805',],
    }

def check_ec(list, string):
    for i in list:
        if i not in string:
            return 'E'
    return '-'
# End

def check_ae(list, string):
    allcaps = string.upper()
    for i in list:
        if i == '10V' and '16V' in allcaps:
            pass  # higher voltage OK
            # print(list)
            # print(string)
        elif i not in allcaps and i not in ['CAP', 'CER',]:  # ignore meaningless tokens
            return 'E'
    return '-'
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
        desc = desc.replace('NPO', 'C0G/NP0')  # fix NPO typo
        desc = desc.replace('2200PF', '2.2NF')  # replace PF value
        desc = desc.replace('3300PF', '3.3NF')  # replace PF value
        desc = desc.replace('10000PF', '0.01UF')  # replace PF value
        ecpn = 'xx-xxxxx'
        ecpn_info = ''
        if id == 'EdgeCortix':
            try:
                ecpn_info = ecpl[row[ecpn_col]]
                ecpn = row[ecpn_col]
            except:
                ecpn_info = 'Need to add ' + row[ecpn_col]
                ecpn = 'xx-xxxxx'
        else:
            ecpn_info = ''
        if refdes.startswith('C') and not refdes.endswith(')'):  # skip DNP
            info[filename][refdes.split(',')[0]] = [ecpn, desc, ecpn_info]

# print(info)
# print(info[filenames[0]]['C1'])
# print(info[filenames[1]]['C1'])

with open('temp.log', 'w') as f:
    f.write('\n')
for refdes in info[filenames[0]]:
    this_info = info[filenames[0]][refdes]
    that_info = info[filenames[1]][refdes]
    log = this_info[0] + ' ' + refdes.ljust(12) + this_info[1].ljust(35) + ' | ' + check_ec(this_info[2], this_info[1]) + ' | ' + check_ae(this_info[2], that_info[1]) + ' | ' + str(info[filenames[1]][refdes])
    print(log)
    with open('temp.log', 'a') as f:
        f.write(log + '\n')
# EOF
