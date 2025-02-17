import os
import sys
import time
try:
    import pyperclip  # requires pip install pyperclip
except:
    print('This script requires pyperclip')
    os.system('PAUSE')
    sys.exit(0)

info = [
    ['jam',        'zoom',    """https://us02web.zoom.us/j/7034311136?pwd%3DcVRib2RwTk9HcTBuQXZvcUpNb3ZuZz09&sa=D&source=calendar&ust=1731178891129279&usg=AOvVaw193s4XvVVrFYkVRRfDVcf7"""],
    ['040',        '.py',     """s2lp-s2m2_0p4p0x1.hex"""],
    ['04LDO',      '.py',     """s2lp-s2m2_0p4p0_DIS-P0V8-LDO_X1.hex"""],
    ['071',        '.py',     """s2_bmc_0_7_1_secondary.hex"""],
    ['101',        '.py',     """s2_bmc_1_0_1_secondary.hex"""],
    ['102',        '.py',     """s2_bmc_1_0_2_secondary.hex"""],
    ['104',        '.py',     """s2_bmc_1_0_4_secondary.hex"""],
    ['110',        '.py',     """s2_bmc_1_1_0_secondary.hex"""],
    ['SWindows',   '.py',     """SW.hex"""],
    ['SLinux',     '.py',     """SL.hex"""],
    ['first search term', 'second search term or ".py" if none required', 'clipboard image or filename']]


def readfile(filename):
    print('Reading: ' + filename)
    try:
        with open(filename, 'r') as f:  # open file
            s = f.read()  # read file
    except:
        print('\nFile Error\n')  # print for clarity
        s = 'File Error'  # most likely file doesn't exist
    return s  # return file contents
# End


thisfile = os.path.basename(__file__)
if thisfile in ['xyclip.py',]:  # list of filenames that won't even be checked
    print('\nThis script must be renamed to generate a clipboard image.\n')
    os.system('PAUSE')
else:
    print(thisfile)
    for searchlist in info:
        x = searchlist[0]
        y = searchlist[1]
        z = searchlist[2]
        if x in thisfile and y in thisfile:
            print('Found search terms: ' + x + ' & ' + y)
            if 'hex2clip' in thisfile:  # could add other keywords that cause readfile to happen
                z = readfile(z)
            pyperclip.copy(z)  # place image on clipboard
            break
    print('Clipboard image is now accessible, assuming search terms matched. Script exiting in five seconds...')
    time.sleep(5)

# End
