# this script compares old and new netlists
# 'old.new.py' compares 'old.NET converted to.dict' and 'new.NET converted to.dict'

import os
import ast
import sys


def compare_nets(stringa, stringb, infoa, infob):
    match = 0
    total = 0
    print(stringa + ' -> ' + stringb + ' (Nets)')
    for net in infoa:
        try:
            a = infoa[net]
            total = total + len(a)
            b = infob[net]
            if a != b:  # might require sorting?
                print('Mismatch in: ' + net)
            else:
                match = match + 1
        except:
            print('Net not found: ' + net)
    print('Matching nets: ' + str(match))
    print('Total nodes: ' + str(total))
    print() # blank line between sections
# End


def compare_nodes(stringa, stringb, infoa, infob):
    match = 0
    log = ''
    print(stringa + ' -> ' + stringb + ' (Nodes)')
    for node in infoa:
        try:
            a = infoa[node]
            b = infob[node]
            if a != b:  # might require sorting?
                log = log + 'Mismatch: ' + a + ' -> ' + b + ' (' + node + ')\n'
            else:
                match = match + 1
        except:
            print('Node not found: ' + node)
    print('Total nodes: ' + str(match))
    with open(stringa + '.' + stringb + '.log', 'w') as f:
        f.write(log)
    print() # blank line between sections
# End


def getnodes(info):
    nodes = {}
    for net in info:
        for node in info[net]:
            nodes[node[0]+'.'+node[1]] = net  # dev.pin is the key and net is the value
    return nodes
# End


# get filenames
splitondot = os.path.basename(__file__).split('.')
if len(splitondot) == 3:
    oldfilename = splitondot[0]
    newfilename = splitondot[1]
else:
    print('Filename must be old.new.py')
    os.system("PAUSE")
    sys.exit()
ext = '.NET converted to.dict'

# open old
try:
    with open(oldfilename + ext, 'r') as f:
        oldfile = f.read()
        oldinfo = ast.literal_eval(oldfile)
except:
    print('Error reading: ' + oldfilename + ext)
    oldinfo = {'nets': []}  # likely due to file not found
    print()
oldnets = oldinfo['nets']
oldnodes = getnodes(oldnets)

# open new
try:
    with open(newfilename + ext, 'r') as f:
        newfile = f.read()
        newinfo = ast.literal_eval(newfile)
except:
    print('Error reading: ' + newfilename + ext)
    newinfo = {'nets': []}  # likely due to file not found
    print()
newnets = newinfo['nets']
newnodes = getnodes(newnets)

# start of script
print('Netlist and Node Compare Utility by HJS\n')

# net analysis
compare_nets(oldfilename, newfilename, oldnets, newnets)
compare_nets(newfilename, oldfilename, newnets, oldnets)

# node analysis
compare_nodes(oldfilename, newfilename, oldnodes, newnodes)
compare_nodes(newfilename, oldfilename, newnodes, oldnodes)

os.system("PAUSE")
# EOF
