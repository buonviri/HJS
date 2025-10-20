# ae00 filters aetina logs

import os
import re

ver = '0.01'  # TBD

def debug(s):
    print(s.strip())

def validate(raw, filtered):
    status = True
    patterns = [
        'FTDI: [0-9]{8}',
        'BIST 0: sakura',  # test case for wrapped saku\nra instance
        ]
    for pattern in patterns:
        a = re.findall(pattern, raw)
        b = re.findall(pattern, filtered)
        if a == b:
            print('Match: ' + str(a))
        else:
            print('Error: ' + str(a) + ' | ' + str(b))
            status = False
    return status
# End function

# read all files
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                rawlines = f.read()
                filteredlines = rawlines.replace('\n','')  # remove ALL newlines
                lines = rawlines.split('\n')  # split into list of lines
                if validate(rawlines, filteredlines):
                    print('\nData is valid')
                else:
                    print('\nData is corrupted')
                print()
                with open(filename + ' rawlines.txt', 'w', encoding='utf-8') as f:
                    f.write(rawlines)
                with open(filename + ' filteredlines.txt', 'w', encoding='utf-8') as f:
                    f.write(filteredlines + '\n')
                with open(filename + ' lines.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))

# EOF
