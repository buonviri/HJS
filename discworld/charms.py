# instructions:
# copy results of alias charms = 'locate charms' to clipboard, then run this script

import os
import pyperclip

clip = pyperclip.paste()
kept = clip.split('.')
required = {
# Bp = wepone
# Genua = weptwo
# ironwood buckler is a copy of AM
    'dham': 0,             # Am
    'copperheadcharm': 0,  # Mines
    'dhsoyin': 0,          # soYin
    'dhsam': 0,            # Sams
    'dhkom': 0,            # Kom
    'dhjulie': 0,          # Julie
    'dhdjb': 0,            # Djb
    'dhquota': 0,          # Quota
    'dhapex': 0,           # 403
    'dhhorse': 0,          # Horse
    'dhfalaf': 0,          # Laughing
    'dhwerks': 0,          # Werks
    'dhoc': 0,             # Oc
    'dhcharms': 0,         # Charms
    'dhprospect': 0,       # Prospect
    'dhfiligree': 0,       # Filigree
    'dhzzz': 0,            # Zzz
    'dhleg': 0,            # inside leg?
     # unused:
    'gold swamp dragon charm (keeping) is in': 0,
    'gold raven charm (keeping) is in': 0,
    'gold yeti charm (keeping) is in': 0,
    'gold jackal charm (keeping) is in': 0,
    'gold lamb charm (keeping) is in': 0,
    'gold needle charm (keeping) is in': 0,
    'gold black widow spider charm (keeping) is in': 0,
    'gold sailor charm (keeping) is in': 0,
    'gold scorpion charm (keeping) is in': 0,
    'gold fishing rod charm (keeping) is in': 0,
    'gold new moon charm (keeping) is in': 0,
    'gold scarf charm (keeping) is in': 0,
    'fake charm': 0,       # THE END
}

print('\nFound:')
for raw in kept:
    mismatch = True
    line = raw.strip()
    for k in required:
        if k in line:
            print('  ' + k)  # indent
            mismatch = False
            del required[k]
            break
    if mismatch and len(line) > 0:  # skip blank lines
        print('\nMismatch: ' + line + '\n')

print('\nMissing:')
print(required)
print()

os.system("PAUSE")

#EOF
