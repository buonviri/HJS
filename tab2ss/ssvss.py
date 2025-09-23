# compare ss files named a.list and b.list
# use tab2ss.py --list to create each file and rename it appropriately
# 'a' is old and 'b' is new

import ast

# constants
refdescol = {'EdgeCortix': 2, 'Aetina': 6,}  # Aetina requires 6:10 to be concatenated
mfg = 3  # EC only
mpn = 4  # EC only
item = 2  # Aetina only
log = {
    '99': '99 - missing.txt',
    '00': '00 - no aetina info.txt',
    '01': '01 - bad aetina info.txt',
    '06': '06 - incorrect spacing.txt',
    '07': '07 - prefix and suffix.txt',
    '08': '08 - endswith.txt',
    '09': '09 - startswith.txt',
    '10': '10 - perfect match.txt',
    }

def AetinaRefDesMerge(row):  # entire row info is passed, new row is returned
    new_cell = ''
    start_col = refdescol['Aetina']
    for cell in row[start_col:]:  # everything from refdescol to the end
        new_cell = new_cell + cell + ','  # always append a comma, need to deal with it later
    new_cell = new_cell.strip(',')  # remove trailing comma(s) for compare
    if row[start_col] != new_cell:  # something changed
        pass  # print(row[0:start_col] + [new_cell,])  # debug
    return row[0:start_col] + [new_cell,]  # recreate row
# End of function

def mfg_fix(s):  # fix mfg names to match Aetina
    fix = {  # dictionary of mfg name fixes
        # ours: theirs (caps irrelevant)
        'Lite-On Inc.': 'Lite-On',
        'Murata Electronics': 'Murata',
        'Nexperia USA Inc.': 'NEXPERIA',
        'Samsung Electro-Mechanics': 'Samsung',
        'Texas Instruments': 'TI',
        'Vishay Dale': 'Vishay',
        }
    try:
        return fix[s]
    except:
        return s
# End of function

def remove_prefix(s):  # filter Aetina strings
    prefix = [  # list of strings to remove
        # warning: always list ABC DEF before ABC!
        'BEAD',
        'BUCK CONVERTER',
        'CHIP INDUCTOR',
        'CHOKE',
        'LED',
        'LEVEL SHIFTING',
        'LOGIC IC',
        'LPDDR4',
        'MCU',
        'MLCC',
        'MONITOR',
        'OSCILLATOR',
        'POWER SWITCH',
        'REGULATOR',
        'RESISTOR CURRENT',
        'RESISTOR',
        'SENSOR',
        'USB BRIDGE CONTROLLER',
        'ZENER DIODE',
        ]
    for x in prefix:
        if s.startswith(x):
            return s[len(x):].strip()  # also removes leading space if present
    return s  # nothing to remove
# End of function

def remove_suffix(s):  # filter Aetina strings
    suffix = [
        '(WPGA_EC)',
        ]
    for x in suffix:
        if s.endswith(x):
            return s[:len(s)-len(x)]
    return s  # nothing to remove
# End of function

# main()
filenames = ['a.list', 'b.list']
info = {filenames[0]: {}, filenames[1]: {},}  # blank dicts
for filename in filenames:
    refdescount = 0
    dnpcount = 0
    with open(filename, 'r') as f:
        ss = ast.literal_eval(f.read())  # convert to spreadsheet
    if ss[0][0] in ['ECPN',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'EdgeCortix'
    elif ss[0][0] in ['Model',]:  # list of upper left cell values that indicate EdgeCortix format
        id = 'Aetina'
    else:
        id = 'Invalid format'
    print('\n' + id + ': ' + str(ss[0]))
    for row in ss[1:]:  # skip header row
        if id == 'EdgeCortix':
            if row[refdescol['EdgeCortix']].endswith('(DNP)'):
                # print('Removed: ' + row[refdescol['EdgeCortix']])
                row = ['',] * (refdescol[id] + 1)  # blank out info up to refdescol
                mfg_mpn = ''  # blank
                dnpcount = dnpcount + 1
            else:
                mfg_mpn = mfg_fix(row[mfg]).upper() + ':' + row[mpn]  # concatenate to match Aetina format, with mfg fixes
        if id == 'Aetina':
            row = AetinaRefDesMerge(row)  # need to merge some cells for Aetina
            mfg_mpn = remove_suffix(remove_prefix(row[item]))  # Aetina format, with filtering
        refdeslist = row[refdescol[id]].split(',')
        for rawrefdes in refdeslist:
            refdes = rawrefdes.strip()
            if refdes == 'PCB1':
                refdes = 'PWB1'  # fix for Aetina BOM
            if len(refdes) > 0:  # non-blank entries ONLY
                if refdes in info[filename]:  # already exists
                    print('ERROR! Duplicate RefDes: ' + refdes)
                refdescount = refdescount + 1
                info[filename][refdes] = mfg_mpn  # format should contain mfg:mpn, with possible extra chars
    print('  RefDes Count: ' + str(refdescount))
    print('    Info Count: ' + str(len(info[filename])))
    print('     DNP Count: ' + str(dnpcount))

for i in log:
    with open(log[i], 'w') as f:
        f.write(log[i] + '\n')  # overwrite file with filename for now

print('\nComparing...')
lines = 0
for refdes in info[filenames[0]]:
    old = info[filenames[0]][refdes]
    note = ''  # blank note field by default
    try:
        new = info[filenames[1]][refdes]
    except:
        new = ''
    if refdes not in info[filenames[1]]:  # key missing from dict
        i = '99'
    elif len(new) < 1:  # their info is blank
        i = '00'
    elif new == old:  # their info matches our info exactly (after filtering)
        i = '10'
    elif new.startswith(old):  # their info starts with our info
        i = '09'
    elif new.endswith(old):  # their info ends with our info
        i = '08'
    elif old in new:  # their info contains with our info
        i = '07'
    elif old in new.replace(': ', ':'):  # workaround if they have a space after the colon
        i = '07'
        note = 'extra space'
    elif old in new.replace(' : ', ':'):  # workaround if they have a space before AND after the colon
        i = '07'
        note = 'extra space'
    else:  # bad aetina info
        i = '01'
    with open(log[i], 'a') as f:
        f.write(refdes.rjust(6) + ' | ' + old.ljust(50) + ' | ' + new.ljust(50) + ' | ' + note + '\n')
    lines = lines + 1
print('Line Count: ' + str(lines))

# EOF
