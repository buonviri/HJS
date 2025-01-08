"""This script generates a map based on the map.yaml file."""

import os
import ast
import yaml

# user settings
# (1) verbose is ['C', 'TP'], quiet is [] or ['none']
show_list = []  # show or hide C (capacitors) and TP (testpoints)
# (2) True or False
show_all = False  # show all nodes, rather than just mapped one


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
    foo = '[' + node[0] + '.' + node[1] + '] ' + getnet(node)
    print('  ' + ecpn + foo.rjust(30), end='')  # two spaces, eight ECPN length
# End


def printright(node):
    """Print right node."""
    foo = ' -> ' + getnet(node) + ' [' + node[0] + '.' + node[1] + ']'
    print(foo)
# End


def transparent(ecpn):
    """Generate [a,b,b,a] list based on ECPN."""
    if ecpn == 'EC-0018R':
        return ['1', '4', '4', '1']  # pins 1 and 4 are in/out
    elif ecpn == 'EC-0001U':
        return ['D1', 'E1', 'E1', 'D1']  # first phase only
    elif ecpn == 'EC-0003J':
        return ['1', '2', '2', '1']  # fan header happens to match RLC
    elif ecpn == 'EC-0046U':
        return ['A1', 'A2', 'A2', 'A1']  # fan header happens to match RLC
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


def display(startnode):
    startstring = startnode.split('.')
    startinfo = (startstring[0], startstring[1])  # tuple
    startnet = ''
    for net in info['nets']:
        for node in info['nets'][net]:
            if node == startinfo:  # compare tuples
                startnet = net
                print('Name:  ' + startnet)  # insert blank line
    # debug:
    # print('Temp: ', end='')
    # print(info['nets'][startnet])
    for node in info['nets'][startnet]:
        try:
            ecpn = info['comps'][node[0]]['PART_NUMBER']
        except:
            ecpn = '--ECPN--'
        ab = transparent(ecpn)  # get a -> b and b -> a transparency
        newnode = ('dev','pin')  # default in case no match is found
        for i in range(2):
            left = ab[2 * i]  # left pin number
            if node[1] == left:
                right = ab[2 * i + 1]  # right pin number
                newnode = (node[0], right)
        if show(node):
            left_raw = '[' + node[0] + '.' + node[1] + '] ' + getnet(node)
            left_str = '  ' + ecpn + left_raw.rjust(60)
            right_str = ' -> ' + getnet(newnode) + ' [' + newnode[0] + '.' + newnode[1] + ']'
            if newnode == ('dev','pin'):  # new node not found
                if show_all:
                    print(left_str + '    ???')
            else:
                print(left_str + right_str)
# End


""" SCRIPT """


# get info from yaml
try:
    with open('map.yaml', 'r') as f:
        map = yaml.safe_load(f)
except:
    map = {'nodes': [], 'file': 'none'}  # blank-ish dict
try:
    with open(map['file'], 'r') as f:
        info_text = f.read()
    info = ast.literal_eval(info_text)
except:
    print('File not found')
    exit(0)
if 'show_all' in map:
    show_all = map['show_all']  # override default with yaml value
if 'show_list' in map:
    show_list = map['show_list']  # override default with yaml value

# check show status
if 'C' not in show_list:
    print('Info:  Capacitors are hidden')
if 'TP' not in show_list:
    print('Info:  Testpoints are hidden')

# start of main
for mynode in map['nodes']:
    if mynode.startswith('info'):  # allows info string to be displayed
        print('\n' + mynode[4:].strip())  # insert extra newline
    else:
        print('\nNode:  ' + mynode)
        display(mynode)
# end of main

if False:
    os.system("PAUSE")
# EOF
