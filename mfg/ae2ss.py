# ae2ss generates a dictionary and spreadsheet(s) based on all of the aetina log files in the current folder

import os
import pyperclip

ver = '0.70'  # homer

info = {}  # good info
sn_min = 99999999
sn_max = 0
clip = ''  # clipboard

def summarize(lines, dirname, filename):
    global sn_min
    global sn_max
    s = ''  # blank file
    bmc = ''
    serial_lines = ''
    dry_lines = ''
    dry_lines_dupe = ''
    homer_elapsed = ''
    max_pcb_temp = -1
    max_sak_temp = -1
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
    s = s + filename[:-4] + '\t'  # add raw filename minus extension
    s = s + sn_file  # add SN (should be first eight or twelve chars of filename)
    for line in lines:
        line = line.strip()
        if line.startswith('FTDI: ') and sn_file in line:  # FTDI, correct XXXXXYYY was found
            serial_lines = serial_lines + 'F'
        elif line.startswith('iSerial 3 ') and sn_file in line:  # iSerial 3, correct XXXXXYYY was found
            serial_lines = serial_lines + 'i'
        elif line.startswith('Board: ') and sn_ec in line:  # BMC info, correct XXXXX-EC-YYY was found
            serial_lines = serial_lines + 'B'
        elif line.startswith('MAX, '):  # telem info
            telem = line.split(',')  # telem lines are csv format
            tpcb = float(telem[3])
            tsak = float(telem[4])
            if tpcb > max_pcb_temp:
                max_pcb_temp = tpcb
            if tsak > max_sak_temp:
                max_sak_temp = tsak
        elif '[DETR]' in line:  # DRY section
            if len(dry_lines) > 0:  # match was already found
                dry_lines_dupe = dry_lines_dupe + dry_lines
                dry_lines = ''
            dry_lines = dry_lines + '\tD'
        elif '[ResNet50]' in line:  # DRY section
            dry_lines = dry_lines + '\tR'
        elif '[YoloV8]' in line:  # DRY section
            dry_lines = dry_lines + '\tY'
        elif 'Total latency: ' in line and line.endswith(' us'):  # DRY latency
            dry_latency = line.split()[-2]  # store second to last string
            dry_lines = dry_lines + '\t' + '%.0f' % float(dry_latency)
        elif line.startswith('t = ') and line.endswith(' s'):  # Homer chatbot elapsed
            homer_elapsed = line.split()[-2]  # elapsed time in seconds, overwrites existing value
        for bmc_key in bmc_info:
            if bmc_key in line:
                bmc = bmc_info[bmc_key]
    s = s + dry_lines  # add all DRY info
    s = s + '\t' + str(max_pcb_temp) + '\t' + str(max_sak_temp)
    s = s + '\t' + homer_elapsed  # add all homer info
    s = s + '\t' + bmc  # add BMC string
    s = s + '\t' + serial_lines  # add all SN info
    s = s + dry_lines_dupe  # add duplicate(s)
    print(s)  # debug
    return s

# clear summary in case it already exists
with open('_summary.txt', 'w') as f:
    f.write(os.path.abspath(os.getcwd()) + '\n')  # path
    f.write('ae2ss version ' + ver + '\n\n')  # version number

# read all files
filecount = 0
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            filecount = filecount + 1
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                result = summarize(f.readlines(), dirname, filename)
                with open('_summary.txt', 'a') as f:
                    f.write(result + '\n')
                    clip = clip + result + '\n'

# summarize counts
with open('_summary.txt', 'a') as f:
    f.write('\nSN ' + str(sn_min) + ' to ' + str(sn_max) + ' (' + str(sn_max-sn_min+1) + ')\n')  # sn range and expected count
print('\nFile count: ' + str(filecount))  # print file count

# cilpboard
pyperclip.copy(clip)  # place result on clipboard

# EOF

# batch file:
# @echo off
# python.exe C:\EdgeCortix\HJS\mfg\ae2ss.py
# pause
