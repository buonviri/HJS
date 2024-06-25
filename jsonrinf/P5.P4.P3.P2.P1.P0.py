# this script extracts netnames staring with [scriptname]
#   'P3V3.py' extracts P3V3* nets
# lists of prefixes may be separated by '.'
#   'P5.P4.P3.P2.P1.P0.py' lists all nets from 0 to 5 volts

import os
import ast
import pyperclip

tokens = os.path.basename(__file__).split('.')  # get list of tokens
if tokens[-1] == 'py':
    targets = tokens[:-1]
    print('Searching for:\n  ' + str(targets))
else:
    targets = []
    print('Invalid file name')
    print(tokens)

info_text = pyperclip.paste()
info = ast.literal_eval(info_text)

matches = []
for net in info['nets']:
    for target in targets:
        if net.startswith(target):
            matches.append(net)
matches.sort()  # alphabetize

clipboard = '\n'.join(matches)
print(clipboard)
pyperclip.copy(clipboard)

print()
os.system("PAUSE")
# EOF
