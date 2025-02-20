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
    ['.hex2clip',  '.py',     """ SPECIAL CASE """],
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
            if thisfile.endswith('.hex2clip.py'):  # special case for hexfiles
                targetfile = thisfile[:-8]  # remove '2clip.py' leaving proper filename
                z = readfile(targetfile)
            pyperclip.copy(z)  # place image on clipboard
            break
    print('Clipboard image is now accessible, assuming search terms matched. Script exiting in five seconds...')
    time.sleep(5)

# End
