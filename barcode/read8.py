import sys
import msvcrt

separator = '-EC-'

def getbarcode():
    bc = ""
    n = 8
    while len(bc) < n:
        c = msvcrt.getwch() # reads one unicode char at a time
        bc += c
        if len(bc) == 6:
            if bc[5].isdigit():
                n = 8
            elif bc[5] in '-_':  # separators for n=12, typically dash or underscore
                n = 12
            else:
                pass  # could add more checks
    return bc
# End

def validate(bc):
    if bc.startswith('00'):
        return 'Cannot have leading zeroes'
    elif bc.startswith('0'):
        return 'Cannot have a leading zero'
    elif len(bc) == 8:
        if not bc.isdigit():
            return 'Must contain only decimal digits [0-9]'
    elif len(bc) == 12:
        if not bc[0:5].isdigit():
            return 'Lot code must contain only decimal digits [0-9]'
        elif not bc[9:12].isdigit():
            return 'Serial must contain only decimal digits [0-9]'
        elif bc[5:9] != separator:
            return 'Separator must be "' + separator + '"'
    return ''
# End

# Start of script
print()  # blank line
if len(sys.argv) == 2:  # exactly one arg
    barcode = sys.argv[1]  # barcode is only arg
    print('[' + barcode + '] ', end ='')
else:
    barcode = getbarcode()  # read from input
bcerror = validate(barcode)
if bcerror == '':  # no error
    if len(barcode) == 8:
        print('Writing files for: ' + barcode[0:5] + separator + barcode[5:8])
    elif len(barcode) == 12:
        print('Writing files for: ' + barcode)
    else:
        print('Invalid barcode length')
else:  # returned error
    print('Invalid input (' + barcode + ') | ' + bcerror)
# print()  # blank line
