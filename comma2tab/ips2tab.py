import pyperclip

suppress_first = True  # set to false to keep first reading

ips = pyperclip.paste()  # get tab data from clipboard
rows = ips.split('\n')
count = -1  # first row is header, second row should start at zero
new_ips = ''
last_row_was_header = False  # initialize
for row in rows:
    if count < 0:
        new_row = 'index'  # header row, index
    else:
        new_row = str(count)  # start with row count
    cells = row.split(',')
    if len(cells) > 1:  # skip blank rows which will have one list entry
        for cell in cells:
            val = cell.strip()
            new_row = new_row + '\t' + val  # add tab and cell string
        try:
            float_test = float(val)  # convert last val to float     
            if last_row_was_header and suppress_first:
                last_row_was_header = False  # row was numeric
                new_row = str(count) + '\t' + 'removed'
        except:
            # test: new_row = new_row + '\t' + 'x'
            last_row_was_header = True
        new_ips = new_ips + new_row + '\n'  # add newline and add to ips
        count = count + 1
pyperclip.copy(new_ips)  # place back on clipboard

# EOF
