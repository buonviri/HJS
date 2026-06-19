# copy results of 'shop' alias to clipboard, then run this script

import os
import pyperclip

filtered = []
discard = []
clip = pyperclip.paste()

clip = clip.replace('You count', '')
clip = clip.replace('On the elderly kitchen table are', '')
clip = clip.replace('with a total of', ',')
clip = clip.replace('\n', ',')
clip = clip.replace('and a', ', a')  # serial comma workaround
clip = clip.replace('and one', ', one')  # serial comma workaround
clip = clip.replace('and two', ', two')  # serial comma workaround
clip = clip.replace('and three', ', three')  # serial comma workaround
clip = clip.replace('and four', ', four')  # serial comma workaround
clip = clip.replace('and five', ', five')  # serial comma workaround

def tee(s):  # print to screen and also write to log
    print(s)
    with open('shop.log', 'a') as f:
        f.write(s + '\n')

items = clip.split(',')
for line in items:
    if len(line) < 2:
        pass  # blank line
    elif line.startswith('Queued'):
        pass  # meaningless line
    elif line.endswith(' items.'):
        pass  # meaningless line
    else:
        line=line.replace('.','')  # remove ending period, might remove others as well
        filtered.append(line.strip())
        tee(line)

print()
os.system("PAUSE")

#EOF
