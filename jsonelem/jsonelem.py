import os


def convert(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    item = '0'  # allegro starts at 1
    refdes = 'None'
    print('  ' + lines[0].strip())  # first line should be count
    for line in lines:
        stripped = line.strip()
        if stripped.startswith ('Item '):
            item = stripped.split()[1]  # token after 'Item' keyword is item number
            refdes = 'None'
            # print('  ' + item, end="")  # debug
        xequy = stripped.split('=')
        if len(xequy) > 1 and xequy[0].strip() == 'COMMENT':  # at least two entries and type is comment
            print('  Item ' + item + ' (' + refdes + '): ' + xequy[1].strip())  # if more than two entries, only prints first
        acolb = stripped.split(':')
        if len(acolb) > 1 and acolb[0].strip() == 'Designator':  # at least two entries and type is designator
            refdes = acolb[1].strip()  # if more than two entries, only stores first
    return item  # last item is also item count
# End

# start of script
print()  # blank line to separate from prompt
for filename in os.listdir():  # only look in current folder
    n = filename.lower()  # only used for checking extension
    if n.endswith('.txt'):
        name = filename[:-4]  # remove extension
        print('Converting ' + filename)
        itemcount = convert(filename)
        print('  Found ' + itemcount + ' item(s)')

print()
os.system("PAUSE")
# EOF
