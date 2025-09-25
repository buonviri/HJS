# copy results of 'csw' alias to clipboard, then run this script

import os
import pyperclip

filtered = []
discard = []
clip = pyperclip.paste()
required = {
    'catnip': True,
    # 'sorrel': True,
    # 'marjoram': True,
    # 'nutmeg': True,
    # 'rosemary': True,
    # 'aniseed': True,
    'curry powder': True,
    'oregano': True,
    'thyme': True,
    'cloves': True,
    'caraway': True,
    'ginger': True,
    'parsley': True,
    'turmeric': True,
    'fennel': True,
    'saffron': True,
    'cardamom': True,
    'methi': True,
    'sumac': True,
    'garlic': True,
    'sea salt': True,
    'cumin': True,
    'black pepper': True,
    'basil': True,
    'cinnamon': True,
    'sage': True,
    'coriander': True,
}

clip = clip.replace('You count', '')
# print(clip)
clip = clip.replace('with a total of', ',')
# print(clip)
clip = clip.replace('wardrobe and about', 'wardrobe , about')
# print(clip)
clip = clip.replace('handful ', '***HANDFUL*** ')
# print(clip)
clip = clip.replace('pinch', '***PINCH***')
# print(clip)
clip = clip.replace('item.', 'item,')
# print(clip)
clip = clip.replace('items.', 'items,')
# print(clip)
clip = clip.replace('\n', ',')
# print(clip)

handfuls = clip.split(',')
for line in handfuls:
    if line.endswith('items') or line.endswith('item'):
        discard.append(line.strip())
        print('END: ' + line)
    elif len(line) < 2:
        pass  # blank line
    elif line.startswith('Queued'):
        pass  # meaningless line
    else:
        filtered.append(line.strip())
        print(line)
# skip for text-only version
# pyperclip.copy('\n'.join(filtered) + '\n' + '\n'.join(discard))

print()  # blank line to separate warnings and/or pause
for f in filtered:
    if ('-one handfuls' in f or '-two handfuls' in f or '-three handfuls' in f or '-four handfuls' in f or 
        '-five handfuls' in f or '-six handfuls' in f or '-seven handfuls' in f or '-eight handfuls' in f or 
        '-nine handfuls' in f):
        pass  # prevent next line from triggering if QTY is 20+
    elif ('one handful' in f or 'two handfuls' in f or 'three handfuls' in f or 'four handfuls' in f or
          'five handfuls' in f or 'six handfuls' in f or 'seven handfuls' in f or 'eight handfuls' in f or
          'nine handfuls' in f):
        print('Warning: ' + f[6:-26])  # remove leading 'about' and trailing 'wardrobe'
    for k in required:
        if k in f:
            del required[k]
            break
missing = 'Missing:'
for k in required:
    missing = missing + ' ' + k
if len(missing) == 8:  # nothing was appended
    missing = missing + ' none'
print(missing)
print()

os.system("PAUSE")

#EOF
