# ae2ss generates a dictionary and spreadsheet(s) based on all of the aetina log files in the current folder

import os

ver = '0.20'
info = {}  # good info

def summarize(lines, dirname, filename):
    s = ''  # blank file
    bmc = ''
    serial_lines = {  # keys are start string of line, values are lists of the remainder of the line
        'FTDI: ': [],
        'iSerial 3 ': [],
        }
    bmc_info = {  # keys are prodtest string, values are summary entries
        'Secondary image, Revision 2.0.3': '[S203]',
        }
    sn_file = filename[0:8]  # decimal SN
    sn_ec = filename[0:5] + '-EC-' + filename[5:8]  # full string SN
    s = s + filename + '\n'  # add raw filename
    s = s + sn_file + ' '  # add SN (should be first eight chars of filename) and trailing space
    for line in lines:
        line = line.strip()
        for serial in serial_lines:
            if line.startswith(serial):
                sn_line = line[len(serial):]  # get SN from line
                if sn_line == sn_file:
                    serial_lines[serial].append('-')  # correct eight-digit serial was found
                else:
                    serial_lines[serial].append(sn_line)  # add to lines
        if line.startswith('Board: ') and sn_ec in line:  # BMC info, correct XXXXX-EC-YYY was found
            serial_lines[serial].append('+')
        for bmc_key in bmc_info:
            if bmc_key in line:
                bmc = bmc_info[bmc_key]
    for serial in serial_lines:
        s = s + ''.join(serial_lines[serial])  # add all SN instances without spaces
    s = s + bmc  # add BMC string
    print(s)  # debug
    with open('summary.txt', 'a') as f:
        f.write(s + '\n')

# clear summary in case it already exists
with open('summary.txt', 'w') as f:
    f.write(os.path.abspath(os.getcwd()) + ' [' + ver + ']\n\n')  # path and version number

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

""" batch file:
@echo off
python.exe C:\EdgeCortix\HJS\mfg\ae2ss.py
pause
"""
