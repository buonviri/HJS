# Rev 1.00: first integrated release

# this script combines two or more timestamped csv files into one, sorted by time

# put all csv files in a folder with this script (or a batch file pointing to the script)
# the number of columns of data and desired locations must be entered below
topology = {3: 'left', 72: 'right'}

import os
import pyperclip

outfile = 'merged.csv'
filelist = []  # blank list
for filename in os.listdir():
    if filename.endswith('.csv') and filename != outfile:
        filelist.append(filename)

blanks = {}  # will be filled with commas
for n in topology:
    minusone = n - 1
    blanks[topology[n]] = ','*minusone  # blank comma strings, one less than data length

csv = {}  # empty dict
index = {'left': 0, 'right': 1}  # the left half is index 0, right half is index 1
for filename in filelist:
    with open (filename, 'r') as f:
        lines = f.readlines()
        commas = lines[0].count(',')
        if commas in topology:
            location = topology[commas]  # left or right
            print('\nFound ' + location + ': ' + filename) 
        else:
            print('\nUnexpected count: ' + str(commas))
            break
        for line in lines:
            line = line.strip()  # remove newline
            tsdata = line.split(',', 1)  # split once to isolate timestamp
            ts = tsdata[0]
            data = tsdata[1]
            if ts in csv:
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
with open(outfile, 'w') as f:
    for tsval in timestamps:
        ts = hex(tsval)[2:]  # convert to hex and remove the 0x portion
        out = out + ts + ',' + csv[ts][0] + ',' + csv[ts][1] + '\n'
    f.write(out)

# print(csv)
pyperclip.copy(out.replace(',', '\t'))  # replace comma with tab for clipboard

print()
os.system('PAUSE')

# EOF
