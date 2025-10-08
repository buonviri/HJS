# ae2ss generates a dictionary and spreadsheet(s) based on all of the aetina log files in the current folder

import os

info = {}  # good info

def summarize(lines, dirname, filename):
    f = ''  # blank file
    startdict = {  # keys are start string of line, values are lists of the remainder of the line
        'FTDI: ': [],  # serial number
        # 'PCIe: ': [],  # PCIe info
        'iSerial 3 ': [],  # serial number
        # 'MAX,': [],  # stats
        }
    f = f + filename + ': '  # add raw filename
    f = f + '[' + filename[0:8] + ']'  # add SN, should be first eight chars of filename
    for line in lines:
        line = line.strip()
        for start in startdict:
            if line.startswith(start):
                startdict[start].append(line[len(start):])
    for start in startdict:
        f = f + ' ' + ' '.join(startdict[start])  # add all SN instances
    print(f)

# read all files
filecount = 0
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            filecount = filecount + 1
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                summarize(f.readlines(), dirname, filename)

print('\nFile count: ' + str(filecount))  # print file count

# EOF

# batch file:
# @echo off
# python.exe C:\EdgeCortix\HJS\mfg\ae2ss.py
# pause
