import os
import time
import pyperclip

info = [
    ['jam', 'zoom', """https://us02web.zoom.us/j/7034311136?pwd%3DcVRib2RwTk9HcTBuQXZvcUpNb3ZuZz09&sa=D&source=calendar&ust=1731178891129279&usg=AOvVaw193s4XvVVrFYkVRRfDVcf7"""],
    ['first search term', 'second search term or ".py" if none required', 'clipboard image']]

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
            print('Found: ' + x + ' ' + y)
            pyperclip.copy(z)  # place image on clipboard
            break
    time.sleep(3)

# End
