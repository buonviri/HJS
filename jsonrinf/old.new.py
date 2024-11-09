# this script compares old and new netlists
# 'old.new.py' compares 'old.NET converted to.dict' and 'new.NET converted to.dict'

import os
import ast
import sys

splitondot = os.path.basename(__file__).split('.')
if len(splitondot) == 3:
    oldfilename = splitondot[0]
    newfilename = splitondot[1]
else:
    print('Filename must be old.new.py')
    os.system("PAUSE")
    sys.exit()
ext = '.NET converted to.dict'

try:
    with open(oldfilename + ext, 'r') as f:
        oldfile = f.read()
        oldinfo = ast.literal_eval(oldfile)
except:
    print('Error reading: ' + oldfilename + ext)
    oldinfo = {'nets': []}  # likely due to file not found
    print()

try:
    with open(newfilename + ext, 'r') as f:
        newfile = f.read()
        newinfo = ast.literal_eval(newfile)
except:
    print('Error reading: ' + newfilename + ext)
    newinfo = {'nets': []}  # likely due to file not found
    print()

match = 0
total = 0
print('old -> new')
for net in oldinfo['nets']:
    try:
        a = oldinfo['nets'][net]
        total = total + len(a)
        b = newinfo['nets'][net]
        if a != b:  # might require sorting?
            print('Mismatch in: ' + net)
        else:
            match = match + 1
    except:
        print('Net not found: ' + net)
print('Matching nets: ' + str(match))
print('Total nodes: ' + str(total))

print()  # blank line between sections

match = 0
total = 0
print('new -> old')
for net in newinfo['nets']:
    try:
        a = newinfo['nets'][net]
        total = total + len(a)
        b = oldinfo['nets'][net]
        if a != b:  # might require sorting?
            print('Mismatch in: ' + net)
        else:
            match = match + 1
    except:
        print('Net not found: ' + net)
print('Matching nets: ' + str(match))
print('Total nodes: ' + str(total))

print()
os.system("PAUSE")
# EOF
