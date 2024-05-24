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


def VerifyAttribute(dict, k, s0, s1):
    for a in dict['comps'][k]['attributes']:
        if a[0] == s0 and a[1] == s1:
            return True
    return False
# End

def GetKeys(files):
    bomkeys = []
    netkeys = []
    # BOM
    with open(files[0], 'r') as f:
        file = f.read()
    dict = ast.literal_eval(file)
    for k in dict:
        bomkeys.append(k)
    # NETLIST
    with open(files[1], 'r') as f:
        file = f.read()
    dict = ast.literal_eval(file)
    for k in dict['comps']:
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
            if VerifyAttribute(dict, k, 'BOM_IGNORE', 'true'):
                bom_ignore = bom_ignore + ' ' + k
            else:
                missing = missing + ' ' + k
    if len(bom_ignore) > 0:
        print('  Ignored:' + bom_ignore)
    if len(missing) > 0:
        print('  Missing from BOM:' + missing)
    return bomkeys  # should be the same as netkeys not counting ignores
# End


# start of script
print()  # blank line to separate from prompt
files = GetFiles()
if len(files) == 2:
    print('Analyzing:\n  ' + '\n  '.join(files))
    keys = GetKeys(files)
    print(keys)
    print('Count: ' + str(len(keys)))
else:
    pass

print()
os.system("PAUSE")
# EOF
