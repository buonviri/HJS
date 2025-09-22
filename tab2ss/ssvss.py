# compare ss files named a.list and b.list

import ast

refdes = {'EdgeCortix': 2, 'Aetina': 6,}  # Aetina requires 6:10 to be concatenated

for filename in ['a.list', 'b.list']:
    with open(filename, 'r') as f:
        ss = ast.literal_eval(f.read())  # convert to spreadsheet
    if ss[0][0] in ['ECPN',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'EdgeCortix'
    elif ss[0][0] in ['Model',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'Aetina'
    else:
        id = 'Invalid format'
    print('\n' + id)
    print(ss[0])
    for row in ss:
        if row[refdes[id]] in ['PWB1', 'PCB1', ]:  # list of PWB refdes
            print(row)
# EOF
