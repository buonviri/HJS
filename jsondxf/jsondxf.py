"""Convert all dxf files in current folder to json format."""

import os

pause = False  # set to true to pause before exist, false to exit instantly
replace_codes = False  # set to true to replace codes with strings
print_entities = False  # set to true to print all entities during execution
print_comments = True  # set to true to print all comments during execution

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
    if replace_codes:
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
           'the__end': []}  # create blank dict
    section = '_errors_'  # default to error section
    for i in range(pairs):
        rawkey = lines[i*2].strip()  # every other line, no whitespace
        key = replace(rawkey)  # replace key with meaningful string
        val = lines[i*2+1].strip()  # every other line +1, no whitespace
        if rawkey in ['10', '20', '30', '11', '21', '31']:  # key is XYZ coord
            kcv = (key, val.rjust(7))  # key comma val, with padding
        else:
            kcv = (key, val)  # key comma val, no padding
        if rawkey == '999':  # indicates comment
            foo['comments'].append(kcv)  # add tuple to list
        elif rawkey == '0' and val == 'SECTION':
            foo['sections'].append(kcv)  # add tuple to list
            section = '_errors_'
        elif rawkey == '0' and val == 'ENDSEC':
            foo['sections'].append(kcv)  # add tuple to list
            section = '_errors_'
        elif rawkey == '0' and val == 'EOF':
            foo['the__end'].append(kcv)  # add tuple to list
            section = '_errors_'
        else:
            if section == '_errors_':
                if rawkey == '2':
                    section = val
                    foo[section] = []  # add new list for this section
                    infotuple = ('2', section)  # tuple containing info
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
    if print_comments:
        for i in dxf['comments']:
            print('  ' + i[0] + ': ' + i[1] + '\n')
    # print(dxf['sections'])
    if print_entities:
        linecount = 0
        for i in dxf['ENTITIES']:
            if i[0] == '0':  # start of new entry
                print()  # add newline
                if i[1] == 'LINE':  # could check for more types here
                    linecount = linecount + 1
            print(i[0] + ': ' + i[1] + '  ', end='')  # print key and value without newline
        print('\n  Line count: ' + str(linecount))
    with open(filename + ' converted to.txt', 'w') as f:
        for k in ['sections', 'the__end']:  # keys in dxf dictionary that should be printed
            # f.write('   ---   ' + k + '   ---   ' + '\n')  # debug separator
            for kcv in dxf[k]:  # key,val pairs in list
                f.write(kcv[0] + '\n')
                f.write(kcv[1] + '\n')
                if kcv[0] == '2':
                    try:
                        section = dxf[kcv[1]]  # only succeeds if section is also a dict entry
                        for section_kcv in section:
                            f.write(section_kcv[0] + '\n')
                            f.write(section_kcv[1] + '\n')
                    except:
                        pass

if pause:
    print()
    os.system('PAUSE')
# EOF
