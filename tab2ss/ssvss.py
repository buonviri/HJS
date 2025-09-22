# compare ss files named a.list and b.list
# use tab2ss.py --list to create each file and rename it appropriately
# 'a' is old and 'b' is new, although the order shouldn't matter

import ast

# constants
refdescol = {'EdgeCortix': 2, 'Aetina': 6,}  # Aetina requires 6:10 to be concatenated

def AetinaRefDesMerge(row):  # entire row info is passed, new row is returned
    new_cell = ''
    start_col = refdescol['Aetina']
    for cell in row[start_col:]:  # everything from refdescol to the end
        new_cell = new_cell + cell + ','  # always append a comma, need to deal with it later
    new_cell = new_cell.strip(',')  # remove trailing comma(s) for compare
    if row[start_col] != new_cell:  # something changed
        pass  # print(row[0:start_col] + [new_cell,])  # debug
    return row[0:start_col] + [new_cell,]  # recreate row
# End of function

# main()
filenames = ['a.list', 'b.list']
info = {filenames[0]: {}, filenames[1]: {},}  # blank dicts
for filename in filenames:
    refdescount = 0
    dnpcount = 0
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
    for row in ss[1:]:  # skip header row
        if row[refdescol[id]] in ['PWB1', 'PCB1', ]:  # list of PWB refdes
            print(row)
        if id == 'EdgeCortix':
            if row[refdescol['EdgeCortix']].endswith('(DNP)'):
                # print('Removed: ' + row[refdescol['EdgeCortix']])
                row = ['',] * (refdescol[id] + 1)  # blank out info up to refdescol
                dnpcount = dnpcount + 1
        if id == 'Aetina':
            row = AetinaRefDesMerge(row)  # need to merge some cells for Aetina
        refdeslist = row[refdescol[id]].split(',')
        for rawrefdes in refdeslist:
            refdes = rawrefdes.strip()
            if len(refdes) > 0:  # non-blank entries ONLY
                if refdes in info[filename]:  # already exists
                    print('Duplicate RefDes: ' + refdes)
                refdescount = refdescount + 1
                info[filename][refdes] = 1  # temp
    print('RefDes Count: ' + str(refdescount))
    print('  Info Count: ' + str(len(info[filename])))
    print('   DNP Count: ' + str(dnpcount))

# EOF
