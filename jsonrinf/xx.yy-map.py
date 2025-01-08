"""This script generates a map based on the map.yaml file."""

import os
import ast
import yaml

# user settings
show_list = []  # show or hide C (capacitors) and TP (testpoints)
# verbose is ['C', 'TP'], quiet is []


""" FUNCTIONS """


def getnet(target):
    """Get netname based on node tuple."""
    for net in info['nets']:
        for node in info['nets'][net]:
            if node == target:  # compare tuples
                return net
    return 'NET_NOT_FOUND'
# End


def printleft(ecpn, node):
    """Print left node."""
    foo = node[0] + '.' + node[1] + ': ' + getnet(node)
    print(ecpn + foo.rjust(32), end='')
# End


def printright(node):
    """Print right node."""
    foo = ' -> ' + node[0] + '.' + node[1] + ': ' + getnet(node)
    print(foo)
# End


def transparent(ecpn):
    """Generate [a,b,b,a] list based on ECPN."""
    if ecpn == 'EC-0018R':
        return ['1', '4', '4', '1']  # pins 1 and 4 are in/out
    elif ecpn == 'EC-0003J':
        return ['1', '2', '2', '1']  # fan header happens to match RLC
    else:
        return ['1', '2', '2', '1']  # default (RLC) is 1 -> 2 and 2 -> 1
# End


def show(node):
    """Return true or false based on user setting."""
    if node[0].startswith('C') and 'C' not in show_list:
        return False
    if node[0].startswith('TP') and 'TP' not in show_list:
        return False
    return True
# End


""" SCRIPT """


# get info from yaml
try:
    with open('map.yaml', 'r') as f:
        map = yaml.safe_load(f)
except:
    map = {'start': 'none', 'file': 'none', 'next': 'none'}  # blank-ish dict
startnode = map['start']  # get script name
print('Node:  ' + startnode)
try:
    with open(map['file'], 'r') as f:
        info_text = f.read()
    info = ast.literal_eval(info_text)
except:
    print('File not found')
    exit(0)
print('Next:  ' + map['next'])

# check show status
if 'C' not in show_list:
    print('Info:  Capacitors are hidden')
if 'TP' not in show_list:
    print('Info:  Testpoints are hidden')

# start of main
startstring = startnode.split('.')
startinfo = (startstring[0], startstring[1])  # tuple
startnet = ''
for net in info['nets']:
    for node in info['nets'][net]:
        if node == startinfo:  # compare tuples
            startnet = net
            print('Name:  ' + startnet)
print('Temp: ', end='')
print(info['nets'][startnet])
for node in info['nets'][startnet]:
    ecpn = '--ECPN--'
    try:
        ecpn = info['comps'][node[0]]['PART_NUMBER']
    except:
        pass  # not found
    ab = transparent(ecpn)  # get a -> b and b -> a transparency
    if show(node):
        printleft(ecpn, node)
    if True:
        if node[1] == ab[0]:
            newnode = (node[0], ab[1])
            if show(node):
                printright(newnode)
        elif node[1] == ab[2]:
            newnode = (node[0], ab[3])
            if show(node):
                printright(newnode)
        else:
            if show(node):
                print('    [Non-standard pin]')
    else:
        print()  # add missing newline
# end of script

if False:
    os.system("PAUSE")
# EOF
