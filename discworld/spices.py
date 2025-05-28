import os
import pyperclip

filtered = []
discard = []
clip = pyperclip.paste()

clip = clip.replace('You count', '')
print(clip)
clip = clip.replace('with a total of', ',')
print(clip)
clip = clip.replace('wardrobe and about', 'wardrobe , about')
print(clip)
clip = clip.replace('handful ', '***HANDFUL*** ')
print(clip)
clip = clip.replace('pinch', '***PINCH***')
print(clip)
clip = clip.replace('items.', 'items,')
print(clip)
clip = clip.replace('\n', ',')
print(clip)

handfuls = clip.split(',')
for line in handfuls:
    if line.endswith('items'):
        discard.append(line.strip())
        print('END: ' + line)
    elif len(line) < 2:
        pass  # blank line
    elif line.startswith('Queued'):
        pass  # meaningless line
    else:
        filtered.append(line.strip())
        print(line)
pyperclip.copy('\n'.join(filtered) + '\n' + '\n'.join(discard))

os.system("PAUSE")

#EOF
