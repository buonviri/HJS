import re
import sys
import pprint
import pyperclip

# check args and enable list/dict
for arg in sys.argv:
    if arg in ['-l', '--list']:
        writelist = True
        writedict = False
    elif arg in ['-d', '--dict']:
        writelist = False
        writedict = True
    else:
        writelist = True
        writedict = True
        
ss = []  # whole spreadsheet
sslist = []
ssdict = {}

cells = pyperclip.paste()  # get tab data from clipboard
rows = cells.split('\n')  # split on newline to make rows

goodRows = {}  # record indices of non-blank rows
goodCols = {}  # record indices of non-blank columns

# record entire clipboard as a list of lists, including all blank cells
rowIndex = 0  # track row index
chinese = r'[\u4e00-\u9fff]+'  # regex covering typical chinese char range
for r in rows:  # iterate over all rows
    colIndex = 0  # track column index, resets each time through loop
    row = []  # blank row to store new cells
    cols = r.split('\t')  # split on tab
    for cell in cols:  # iterate over columns
        value_raw = cell.strip()  # remove any whitespace
        value_deg = re.sub(r'\u2103', 'C', value_raw)  # replace degree C chars with C
        value = re.sub(chinese , '+', value_deg)  # replace chinese chars with +
        row.append(value)  # add to row
        if value != '':  # non-blank
            goodRows[rowIndex] = True
            goodCols[colIndex] = True
        colIndex = colIndex + 1  # increment col counter
    ss.append(row)  # add row to spreadsheet
    # print(row)
    rowIndex = rowIndex + 1  # incremenet row counter

# debug
# pprint.pprint(ss)
# print(goodRows)
# print(goodCols)
# print(rowIndex)
# print(colIndex)

# iterate over indices and look for good entries
for r in range(len(ss)):
    row = []  # blank row to store new cells
    for c in range(len(ss[r])):
        if r in goodRows and c in goodCols:
            row.append(ss[r][c])  # append if it's a good cell
    if len(row) > 0 and row[-1] != '[tab2ss-ignore]':  # skip blank rows and rows ending in ignore
        sslist.append(row)  # append row to list version
        ssdict[r] = row  # set row index (key) equal to row list (value)

if writelist:
    with open('tab2ss.list', 'w') as f:
        f.write(pprint.pformat(sslist) + '\n')

if writedict:
    with open('tab2ss.dict', 'w') as f:
        f.write(pprint.pformat(ssdict) + '\n')

# EOF
