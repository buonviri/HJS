import os
import ast


def GetFiles():
    bom = ''
    net = ''
    for filename in os.listdir():  # only look in current folder
        n = filename.lower()  # only used for checking extension
        if n.endswith('.dict'):
            # print('Found ' + filename)  # debug
            if '.csv converted to' in n:
                bom = filename
            elif '.net converted to' in n:
                net = filename
    if bom == '' or net == '':
        print('This script requires two files: csv and net, converted to dict.')
        return ['error',]  # list length = 1 implies error
    else:
        return [bom,net]  # list of valid files
# End


def GetDict(filename):
    with open(filename, 'r') as f:
        file = f.read()
    dict = ast.literal_eval(file)
    return dict
# End


def VerifyAttribute(dict, k, s0, s1):
    for a in dict['comps'][k]['attributes']:
        if a[0] == s0 and a[1] == s1:
            return True
    return False
# End


def GetKeys(bom, net):
    bomkeys = []
    netkeys = []
    for k in bom:
        bomkeys.append(k)
    for k in net['comps']:
        netkeys.append(k)
    # print(' '.join(bomkeys))  # debug
    # print(' '.join(netkeys))  # debug
    missing = ''
    for k in bomkeys:
        if k not in netkeys:
            missing = missing + ' ' + k
    if len(missing) > 0:
        print('  Missing from Netlist: ' + missing)
    missing = ''
    bom_ignore = ''
    for k in netkeys:
        if k not in bomkeys:
            if VerifyAttribute(net, k, 'BOM_IGNORE', 'true'):
                bom_ignore = bom_ignore + ' ' + k
            else:
                missing = missing + ' ' + k
    if len(bom_ignore) > 0:
        print('  Ignored:' + bom_ignore)
    if len(missing) > 0:
        print('  Missing from BOM:' + missing)
    return bomkeys  # should be the same as netkeys not counting ignores
# End


def GetColumns(bom, net, keys):
    bom_columns = ['ECPN', 'MFG', 'MPN', 'Description']
    net_columns = ['PART_NUMBER', 'Manufacturer', 'Manufacturer PN', 'Description']
    bom_info = {}
    net_info = {}
    for refdes in keys:
        bom_row = []
        try:  # in case keys didn't match, this could fail
            for column in bom_columns:
                bom_row.append(bom[refdes][column])
            bom_info[refdes] = bom_row
        except:
            pass
        net_row = []
        try:  # in case keys didn't match, this could fail
            for column in net_columns:
                net_row.append(net['comps'][refdes][column])
            if 'BuildOptions' in net['comps'][refdes]:  # may or may not be present
                net_row.append(net['comps'][refdes]['BuildOptions'])
            net_info[refdes] = net_row
        except:
            pass
    combined = {}
    for refdes in keys:  # each line should contain four list elements
        bom_line = 'ERROR'
        net_line = 'ERROR'
        try:
            bom_line = bom_info[refdes]
            net_line = net_info[refdes][0:4]  # remove possible BuildOptions entry
            if len(refdes) > 1:  # should be at least 2
                longrefdes = refdes[0] + refdes[1:].rjust(9, '0')  # assumes only single char refdes
            else:
                longrefdes = refdes
            if bom_line != net_line:
                print('  Mismatch in: ' + refdes + '\n    ' + str(bom_line) + '\n    ' + str(net_line))
            combined[longrefdes] = [refdes,] + net_info[refdes]
        except:
            print('  Error in: ' + refdes + '\n    ' + str(bom_line) + '\n    ' + str(net_line))
    return combined
# End


def WriteFiles(all):
    refdes = []
    for k in all:
        refdes.append(k)
    sorted_refdes = sorted(refdes)
    with open('all.tab', 'w') as f:
        f.write('\t'.join(['RefDes', 'ECPN', 'MFG', 'MPN', 'Description', 'BuildOptions']) + '\n')  # header
        for k in sorted_refdes:
            f.write('\t'.join(all[k]) + '\n')
# End


# start of script
print()  # blank line to separate from prompt
files = GetFiles()
if len(files) == 2:
    print('Analyzing:\n  ' + '\n  '.join(files))
    bom = GetDict(files[0])
    net = GetDict(files[1])
    keys = GetKeys(bom, net)
    # print(keys)  # debug
    print('Count: ' + str(len(keys)))
    all = GetColumns(bom, net, keys)
    WriteFiles(all)
else:
    pass

print()
os.system("PAUSE")
# EOF
