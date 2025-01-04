"""Convert all dxf files in current folder to json format."""

import os

pause = True  # set to true to pause before exist, false to exit instantly


"""FUNCTIONS"""


def getfilelist():
    """Get list of all dxf files in current folder."""
    foo = []  # initialize
    for f in os.listdir():
        if f.endswith('.dxf'):
            foo.append(f)
    return foo
# End


def getlines(foo):
    """Get all lines from text file."""
    with open(foo, 'r') as f:
        lines = f.readlines()
    return lines
# End


def replace(foo):
    """Replace dxf codes with meaningful strings."""
    if foo == '999':
        return 'comment'
    if foo == '5':
        return '#'  # index
    if foo == '10':
        return 'X0'
    if foo == '20':
        return 'Y0'
    if foo == '30':
        return 'Z0'
    if foo == '11':
        return 'X1'
    if foo == '21':
        return 'Y1'
    if foo == '31':
        return 'Z1'
    if foo == '100':
        return 'db'  # handle
    if foo == '330':
        return 'db'  # handle
    return foo  # no match found
# End


def lines2pairs(lines):
    """Convert lines to dict."""
    pairs = len(lines) // 2  # floor division, half the length of the list
    foo = {'_errors_': [],
           'comments': [],
           'sections': [],
           'the__end': []}  # blank dict
    section = '_errors_'  # default to error section
    for i in range(pairs):
        key = lines[i*2].strip()  # every other line, no whitespace
        key = replace(key)  # replace key with meaningful string
        val = lines[i*2+1].strip()  # every other line +1, no whitespace
        if key in ['X0', 'X1', 'Y0', 'Y1', 'Z0', 'Z1']:  # key is XYZ coord
            kcv = (key, val.rjust(7))  # key comma val, with padding
        else:
            kcv = (key, val)  # key comma val, no padding
        if key == 'comment':  # indicates comment
            foo['comments'].append(kcv)  # add tuple to list
        elif key == '0' and val == 'SECTION':
            foo['sections'].append(kcv)  # add tuple to list
            section = '_errors_'
        elif key == '0' and val == 'ENDSEC':
            foo['sections'].append(kcv)  # add tuple to list
            section = '_errors_'
        elif key == '0' and val == 'EOF':
            foo['the__end'].append(kcv)  # add tuple to list
            section = '_errors_'
        else:
            if section == '_errors_':
                if key == '2':
                    section = val
                    foo[section] = []  # add new list for this section
                    infotuple = ('pyname', section)  # tuple containing info
                    foo['sections'].append(infotuple)  # add info tuple
                else:
                    print('ERROR: The first key in a new section must be 2.')
                    print(key)
                    print(val)
            else:
                foo[section].append(kcv)  # add tuple to list
    return foo
# End


# start of script
filelist = getfilelist()
for filename in filelist:
    print('\nAnalyzing: ' + filename)
    lines = getlines(filename)
    dxf = lines2pairs(lines)
    print(dxf['comments'])
    # print(dxf['sections'])
    for i in dxf['ENTITIES']:
        if i[0] == '0':
            print()
        print(i[0] + ': ' + i[1] + '  ', end='')

if pause:
    print()
    os.system('PAUSE')
# EOF
