# copy results of alias kept = 'locate kept things except charms' to clipboard, then run this script

import os
import pyperclip

clip = pyperclip.paste()
kept = clip.split('.')
required = {
    'wepone': 0,  # bacon
    'weptwo': 0,  # bacon
    'thiefcoat':0,  # sailing coat
    'badgelicense': 0,
    'ribbon charm bracelet': 0,
    'mybeads': 0,
    'medicine bag': 0,
    'apexbadge': 0,
    'badgelicense': 0,  # thief licence
    'chestring': 0,
    'floatring': 0,
    'ssc': 0,
    'permalight': 0,
    'thiefthong': 0,  # sailing lingerie
    'dhbaton': 0,
    'rpbaton': 0,
    'dhdrum': 0,  # buckler
    'apexkey': 0,
    'otherkey': 0,  # what is this???
    'mycompact': 0,
    'nonexistent kept thing': 0,
}

print('\nFound:')
for raw in kept:
    mismatch = True
    line = raw.strip()
    for k in required:
        if k in line:
            print('  ' + k)  # indent
            mismatch = False
            del required[k]
            break
    if mismatch and len(line) > 0:  # skip blank lines
        print('\nMismatch: ' + line + '\n')

print('\nMissing:')
print(required)
print()

os.system("PAUSE")

#EOF
