import os
import time
import pyperclip

info = [
    ['jam', 'zoom', """https://us02web.zoom.us/j/7034311136?pwd%3DcVRib2RwTk9HcTBuQXZvcUpNb3ZuZz09&sa=D&source=calendar&ust=1731178891129279&usg=AOvVaw193s4XvVVrFYkVRRfDVcf7"""],
    ['040', '.py', '040'],
    ['071', '.py', '071'],
    ['first search term', 'second search term or ".py" if none required', 'clipboard image']]


def checkforfile(s):

    targets = {
        '040': """s2lp-s2m2_0p4p0x1.hex""",
        '071': """s2_bmc_0_7_1_secondary.hex""",
    }
    if s in targets:  # string is in the list of files to open
        filename = targets[s]
        print('Reading: ' + filename)
        with open(filename, 'r') as f:  # open file
            s = f.read()  # read file
    return s  # return either raw string or file contents
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
            pyperclip.copy(checkforfile(z))  # place image on clipboard
            break
    time.sleep(3)

# End
