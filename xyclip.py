import os
import pyperclip

info = [
    ['jam', 'zoom', """https://us02web.zoom.us/j/7034311136?pwd%3DcVRib2RwTk9HcTBuQXZvcUpNb3ZuZz09&sa=D&source=calendar&ust=1731178891129279&usg=AOvVaw193s4XvVVrFYkVRRfDVcf7"""],
    ['first search term', 'second search term or ".py" if none required', 'clipboard image']]

thisfile = os.path.basename(__file__)
if thisfile in ['xyclip.py',]:
    print('\nThis script must be renamed to generate a clipboard image.\n')
    os.system('PAUSE')
else:
    print(thisfile)
    for searchlist in info:
        if searchlist[0] in thisfile and searchlist[1] in thisfile:
            print('Found: ' + searchlist[0] + ' ' + searchlist[1])
            pyperclip.copy(searchlist[2])
            break
    os.system('PAUSE')

# End
