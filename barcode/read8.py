import msvcrt

separator = '-EC-'

def getbarcode():
    bc = ""
    while len(bc) < 8:
        c = msvcrt.getwch() # reads one unicode char at a time
        bc += c
    return bc
# End

def validate(bc):
    if bc.startswith('00'):
        return 'Cannot have leading zeroes'
    elif bc.startswith('0'):
        return 'Cannot have a leading zero'
    elif not bc.isdigit():
        return 'Must contain only decimal digits [0-9]'
    return ''
# End

# Start of script
barcode = getbarcode()
bcerror = validate(barcode)
if bcerror == '':  # no error
    print('Writing files for: ' + barcode[0:5] + separator + barcode[5:8])
else:
    print('Invalid input (' + barcode + ') - ' + bcerror)

# Add pause?
