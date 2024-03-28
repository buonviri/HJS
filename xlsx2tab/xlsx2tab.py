# instructions:
# run this file in a folder containing one or more xlsx files
# each will be converted to tab data and stored as a new file
# the last file read will be placed on the clipboard as well

import os
import pyperclip
from openpyxl import load_workbook

file_list = []
extensions = ('.xlsm', '.xlsx')  # must be five chars long
for file in os.listdir('.'):
    if file[-5:] in extensions:
        file_list.append(file)

clip = ''  # blank string to store clipboard info
for x in file_list:
    print()
    print('  Reading: ' + x)

    wb = load_workbook(filename=x, read_only=True)  # load as read-only
    ws = wb[wb.sheetnames[0]]  # select the first sheet

    for i in ws.values:
        row = []  # blank string to hold row
        for j in i:
            row.append(j.strip())  # remove unwanted whitespace
        clip = clip + '\t'.join(row) + '\n'

    newfile = x[:-5] + '.tab'
    with open(newfile, "w") as f:
        f.write(clip)
    print('  Writing: ' + newfile)

    # Close the workbook after reading
    wb.close()
    del wb

# copy to clipboard and exit
pyperclip.copy(clip)
print('  Copying: ' + newfile[:-4])  # remove tab extension
print()
os.system('PAUSE')
