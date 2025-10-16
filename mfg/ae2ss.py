# ae2ss generates a dictionary and spreadsheet(s) based on all of the aetina log files in the current folder

import os

ver = '0.40'  # add min/max

info = {}  # good info
sn_min = 99999999
sn_max = 0

def summarize(lines, dirname, filename):
    global sn_min
    global sn_max
    s = ''  # blank file
    bmc = ''
    serial_lines = ''
    bmc_info = {  # keys are prodtest string, values are summary entries
        'Secondary image, Revision 1.1.5': '[S115]',
        'Secondary image, Revision 2.0.3': '[S203]',
        }
    if filename[5:9] in ['-EC-',]:  # check if filename has a separator
        sn_file = filename[0:5] + filename[9:12]  # decimal SN
        sn_ec = filename[0:12]  # full string SN
    else:  # filename does not have a separator
        sn_file = filename[0:8]  # decimal SN
        sn_ec = filename[0:5] + '-EC-' + filename[5:8]  # full string SN
    sn_int = int(sn_file)  # get integer version for min/max
    if sn_int < sn_min:
        sn_min = sn_int
    if sn_int > sn_max:
        sn_max = sn_int
    s = s + filename + '\n'  # add raw filename
    s = s + sn_file + ' '  # add SN (should be first eight or twelve chars of filename) and trailing space
    for line in lines:
        line = line.strip()
        if line.startswith('FTDI: ') and sn_file in line:  # FTDI, correct XXXXXYYY was found
            serial_lines = serial_lines + 'F'
        if line.startswith('iSerial 3 ') and sn_file in line:  # iSerial 3, correct XXXXXYYY was found
            serial_lines = serial_lines + 'i'
        if line.startswith('Board: ') and sn_ec in line:  # BMC info, correct XXXXX-EC-YYY was found
            serial_lines = serial_lines + 'B'
        for bmc_key in bmc_info:
            if bmc_key in line:
                bmc = bmc_info[bmc_key]
    s = s + serial_lines  # add all SN chars
    s = s + bmc  # add BMC string
    print(s)  # debug
    with open('summary.txt', 'a') as f:
        f.write(s + '\n')

# clear summary in case it already exists
with open('summary.txt', 'w') as f:
    f.write(os.path.abspath(os.getcwd()) + '\n')  # path
    f.write('ae2ss version ' + ver + '\n\n')  # version number

# read all files
filecount = 0
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            filecount = filecount + 1
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                summarize(f.readlines(), dirname, filename)

# summarize counts
with open('summary.txt', 'a') as f:
    f.write('\nSN ' + str(sn_min) + ' to ' + str(sn_max) + ' (' + str(sn_max-sn_min+1) + ')\n')  # sn range and expected count
print('\nFile count: ' + str(filecount))  # print file count

# EOF

# batch file:
# @echo off
# python.exe C:\EdgeCortix\HJS\mfg\ae2ss.py
# pause
