import os
import csv
import pprint  # needed for pformat


def GetTokens(x):  # modified to split on comma
    return [ '{}'.format(x) for x in list(csv.reader([x], delimiter=',', quotechar='"'))[0] ]
# end of GetTokens()


def convert(filename):
    out = {}
    header = []  # should get overwritten
    keys = [
        '-',
        'Level',
        'ECPN',
        'Revision',
        'Variant',
        'Quantity',
        'RefDes',
        'MFG',
        'MPN',
        'Distributor',
        'Distributor PN',
        'Description',
        'Part Type'
    ]
    good_keys = [2,7,8,11]
    count = 0
    refdescount = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
    if lines[0].startswith(',Level,'):  # CIP BOM should have a blank column header
        header = lines[0].strip().split(',')
        header[0] = 'n'  # override blank entry
        # print('\n'.join(header))  # debug
    else:
        return 'ERROR - HEADER'
    for line in lines[1:]:
        stripped = line.strip()
        tokens = GetTokens(stripped)
        # print(tokens[6])
        refdeslist = tokens[6].split(',')
        for refdes in refdeslist:
            if refdes in out:
                print('Duplicate RefDes: ' + refdes)
            else:
                refdescount = refdescount + 1
                out[refdes] = {}
                for k in good_keys:
                    out[refdes][keys[k]] = tokens[k]
        count = count + 1
    formatted = pprint.pformat(out, indent=2, width=200)
    # print(formatted)
    print('  Found ' + str(refdescount) + ' reference designators')
    return str(count)  # BOM Line Items
# End


# start of script
print()  # blank line to separate from prompt
for filename in os.listdir():  # only look in current folder
    n = filename.lower()  # only used for checking extension
    if n.endswith('.csv'):
        name = filename[:-4]  # remove extension
        print('Converting ' + filename)
        result = convert(filename)
        if result.startswith('ERROR'):
            print('  ' + result)
        else:
            print('  Found ' + result + ' line item(s)')

print()
os.system("PAUSE")
# EOF
