# syntax is grep.py filename pattern

import os
import sys

prefix = '\ngrep '  # first printed line
if len(sys.argv) == 3:
    filename = sys.argv[1]
    pattern = sys.argv[2]
    result = '[in] ' + filename + ' [find] ' + pattern
    search = True
else:
    result = 'syntax is grep.py filename pattern'
    search = False
print(prefix + result)

if search:
    matches = 0
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if pattern in line:
                print(' |' + line.rstrip() + '|')  # remove trailing spaces only
                matches = matches + 1
        print('Matches: ' + str(matches))
    except:
        print('File not found')

# os.system("PAUSE")  # handled in batch file

# EOF
