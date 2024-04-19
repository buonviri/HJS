# this script combines two or more timestamped csv files into one, sorted by time
# Rev 1.00: first integrated release
# Rev 1.01: added code to ignore header if someone adds one
# Rev 2.00: added multi-pass support

# instructions:
# put all csv files in a folder with this script (or a batch file pointing to this script)
# the number of columns of data and desired locations must be entered below
topology_list = [
    ( {1: 'left', 72: 'right'}, 'merged.csv' ), # tuple containing dict and string
    ]
# valid combos:
#   3+72 for 9182B and statlog
#   1+72 for IPS and statlog

import os

clipboard = False
if os.name == 'nt':  # clipboard only works in windows
    try:
        import pyperclip
        clipboard = True
    except:
        print('\nRequires pyperclip. Use: pip install pyperclip\n')

# get filelist once, then append it after each iteration
filelist = []  # blank list
for filename in os.listdir():
    if filename.endswith('.csv'):  # used to include 'and filename != outfile' but now that can be included
        filelist.append(filename)

def MergeTwoFiles(topology, outputfilename):  # topology is a dict with size:side, size:side
    print('Analyzing: ' + str(filelist))
    blanks = {}  # will be filled with commas
    ignore_width = 0  # store the width of the result so that the error checker can ignore it
    for n in topology:
        ignore_width = ignore_width + n
        minusone = n - 1
        blanks[topology[n]] = ','*minusone  # blank comma strings, one less than data length

    csv = {}  # empty dict
    index = {'left': 0, 'right': 1}  # the left half is index 0, right half is index 1
    for filename in filelist:
        with open (filename, 'r') as f:
            lines = f.readlines()
            try:
                commas = lines[0].count(',')  # fails on blank file
            except:
                commas = -1  # use invalid value to ensure this file gets skipped
            if commas in topology:
                location = topology[commas]  # left or right
                print('\nFound ' + location + ': ' + filename) 
            else:
                if commas == ignore_width:
                    print('\nIgnoring: ' + filename)
                else:
                    print('\nUnexpected count: ' + str(commas))
                if commas < 0:
                    print('  (Usually indicates blank file)')
                break
            for line in lines:
                line = line.strip()  # remove newline
                tsdata = line.split(',', 1)  # split once to isolate timestamp
                ts = tsdata[0]
                data = tsdata[1]
                if ts.startswith('t') or ts.startswith('T'):  # likely a header row starting with time, Timestamp, etc
                    print('  Discarding: ' + line)
                elif ts in csv:
                    # print('Duplicate: ' + ts)
                    if len(csv[ts][index[location]]) > len(blanks[location]):  # real data would be longer than blank string
                        print(' Overwriting:' + csv[ts][index[location]] + '\n With: ' + data)
                    csv[ts][index[location]] = data  # lookup index using location, overwrite blank string
                else:
                    csv[ts] = [blanks['left'], blanks['right']]  # each entry is a list of two strings
                    csv[ts][index[location]] = data  # lookup index using location, overwrite blank string

    timestamps = []
    for ts in csv:
        timestamps.append(int(ts, 16))  # convert to decimal and append to list
    timestamps.sort()  # sort list
    # print(timestamps)

    out = ''
    with open(outputfilename, 'w') as f:
        for tsval in timestamps:
            ts = hex(tsval)[2:]  # convert to hex and remove the 0x portion
            out = out + ts + ',' + csv[ts][0] + ',' + csv[ts][1] + '\n'
        f.write(out)
    filelist.append(outputfilename)  # add in case another iteration happens
    return out

for info in topology_list:
    out = MergeTwoFiles(info[0], info[1])  # pass it the dict and the filename string

# print(csv)
if clipboard:
    pyperclip.copy(out.replace(',', '\t'))  # replace comma with tab for clipboard

print()
if os.name == 'nt':
    os.system('PAUSE')

# EOF
