# instructions:
# put all csv files in a folder with this script (or a batch file pointing to this script)

import os
import pprint

clipboard = False
if os.name == 'nt':  # clipboard only works in windows
    try:
        import pyperclip
        clipboard = True
    except:
        print('\nRequires pyperclip. Use: pip install pyperclip\n')

# get filelist
filelist = []  # blank list
outfile = 'abcd.csv'
for filename in os.listdir():
    if filename.endswith('.csv') and filename != outfile:
        filelist.append(filename)

info = {}
timestamps = []

# header and file types
header_9182B = ',System (W),System (A),System (V)'
header_sjlog = ',Fmin,Fmax,Tmin,Tmax'
header_statlog = ',Sakura (W), S1LP (W), TI (C), LTC (C)'
header_inference = ',inference,set_input,e2e,get_output,dna_compute,pcie_data_transfer,cpu_data_reorder,cpu_ops'
out = 't' + header_9182B + header_sjlog + header_statlog + header_inference + ',timestamp\n'
filetypes = ['9182B', 'sjlog', 'statlog', 'inference']  # order dictates csv order
commacount = {'9182B': 3, 'sjlog': 4, 'statlog': 4, 'inference': 8}

# analyze files
for filename in filelist:
    with open (filename, 'r') as f:
        fileprefix = filename.split('-')[0]  # should be prefix
        if fileprefix in filetypes:
            print('\nFile: ' + filename + '\nType: ' + fileprefix)
        else:
            print('\nFile: ' + filename + ' HAS AN INVALID OR MISSING PREFIX')
            fileprefix = 'ignore'
        info[fileprefix] = {}  # blank dict for each file
        commas = []  # blank list for comma counts
        lines = f.readlines() + ['','']  # add blank lines to guarantee min length, must subtract from count later
        if lines[0].startswith('timestamp'):
            print('  Found Header Row')
        else:
            print('  Missing Header Row (File May Be Invalid)')
        for line in lines[1:]:
            raw_list = line.split(',')
            if len(raw_list) > 1 or len(raw_list[0]) > 1:  # list has two or more entries OR one entry but not blank
                commas.append(len(raw_list))
            stripped_list = [x.strip() for x in raw_list]
            info[fileprefix][stripped_list[0]] = stripped_list[1:]  # add line using timestamp as key
            if len(stripped_list[0]) > 0 and stripped_list[0] != 'timestamp':
                timestamps.append(stripped_list[0])
        # print(commas)
        if len(commas) == 0:  # no entries were found
            commas = [-1]
        if min(commas) == max(commas):
            print('  Comma count: ' + str(min(commas)))
        else:
            print('  Comma counts: ' + str(min(commas)) + ' to ' + str(max(commas)))
        print('  Data Rows: ' + str(len(lines) - 3))  # accounts for header plus the two that were added
timestampvals = [int(x, 16) for x in timestamps]
start_time = min(timestampvals)
end_time = max(timestampvals)
print('\nElapsed Time: '+ str(end_time - start_time))
# pprint.pprint(info)
# print(timestamps)
# print(timestampvals)

# generate a line for every possible timestamp
for t in range(start_time, end_time+1):
    ts = hex(t)[2:]
    out = out + str(t-start_time)  # first column is elapsed time (t)
    for filetype in filetypes:
        try:
            x = info[filetype][ts]
            # print(ts)
            # print(x)]
            if len(x) < commacount[filetype]:  # columns are missing
                print('\nMissing Columns: \'' + ','.join(x) + '\' at timestamp ' + ts)
                x[-1] = x[-1] + ',' * (commacount[filetype] - len(x))  # add extra commas to last item in list
                print('  Replaced with: \'' + ','.join(x) + '\'')
            if filetype == 'statlog':  # only write four columns
                x = [x[-17],x[-12],x[-7],x[-3],]
            out = out + ',' + ','.join(x)
        except:
            out = out + ',' * commacount[filetype]
    out = out + ',' + ts+ '\n'  # add original hex timestamp
# print(out)
# print(csv)

with open(outfile, 'w') as f:
    f.write(out + '\n')

if clipboard:
    pyperclip.copy(out.replace(',', '\t'))  # replace comma with tab for clipboard
    print('\nClipboard contains tab data')
else:
    print('\nClipboard is empty')

print()
if os.name == 'nt':
    os.system('PAUSE')

# EOF
