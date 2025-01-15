# ASSUMNES WINDOWS OS
# rename this script ftdi.n.py where n is the number of serialized objects

import os
# Template

# End of Template


def get_container():
    return os.getcwd().split('\\')[-1]  # get string after final backslash
# End


def get_limit():
    foo = os.path.basename(__file__)
    foolist = foo.split('.')
    if len(foolist) == 3:  # ftdi.n.py should have three objects
        try:
            return int(foolist[1]), len(foolist)  # middle entry as integer, length of string
        except:
            return -1, 0  # invalid entry
    else:
        return -2, 0  # wrong length
# End


lot_code = get_container()
if len(lot_code) in [5,]:  # check if length is in the list of valid lot code lengths
    max_sn, len_sn  = get_limit()
    if max_sn < 1:  # must be at least 1
        print('Invalid max serial number: ' + str(max_sn))
    else:
        print('Generating ' + str(max_sn) + ' serial numbers (' + 'n' * len_sn + ') for lot code: ' + lot_code)
        for sn in range(max_sn):
            print(str(lot_code) + str(sn+1).rjust(len_sn, '0'))  # loop value is zero to n-1, padded with leading zeroes
else:
    print('Invalid lot code: ' + lot_code)

# pause for user input
os.system("PAUSE")

# EOF
