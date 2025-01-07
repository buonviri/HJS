# this script generates a map based on a start node
# 'xx.yy-map.py' extracts the map for device xx pin yy

import os
import ast
import pyperclip

showcaps = False  # set to True to show capacitors


def GetNet(target):  # get netname based on node tuple
    for net in info['nets']:
        for node in info['nets'][net]:
            if node == target:  # compare tuples
                return net
    return 'NET_NOT_FOUND'
# End


def printleft(node):
    foo = node[0] + '.' + node[1] + ': ' + GetNet(node)
    print(foo.rjust(40), end='')
# End


def printright(node):
    foo = '  ' + node[0] + '.' + node[1] + ': ' + GetNet(node)
    print(foo)
# End


scriptname = os.path.basename(__file__)  # get script name
# scriptname = 'P1.A2-map.py'  # optional override
# scriptname = 'R3.4-map.py'  # optional override
# scriptname = 'L41.1-map.py'  # optional override
if scriptname.endswith('-map.py'):
    startnode = scriptname[:-7]
    print('Start Node: ' + startnode)
else:
    print('Rename file "device.node-map.py" and try again.')
    exit(0)

# TODO: filename should be searched instead
with open('S2LP.NET converted to.dict', 'r') as f:
    info_text = f.read()
info = ast.literal_eval(info_text)

# start of script
startstring = startnode.split('.')
startinfo = (startstring[0], startstring[1])  # tuple
startnet = ''
for net in info['nets']:
    for node in info['nets'][net]:
        if node == startinfo:  # compare tuples
            startnet = net
            print('       Net: ' + startnet)
print('[debug]')
print(info['nets'][startnet])
for node in info['nets'][startnet]:
    if showcaps or node[0][0] != 'C':
        printleft(node)
    if node[0][0] in 'RLC':  # first char indicates res, ind, cap
        if node[1] == '1':
            newnode = (node[0], '2')
            if showcaps or node[0][0] != 'C':
                printright(newnode)
        elif node[1] == '2':
            newnode = (node[0], '1')
            if showcaps or node[0][0] != 'C':
                printright(newnode)
        else:
            if showcaps or node[0][0] != 'C':
                print('  Non-standard pin')
    else:
        print()  # add missing newline
# end of script

if True:
    os.system("PAUSE")
# EOF
