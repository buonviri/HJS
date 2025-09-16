import os
import pprint
import pyperclip

raw_clip = pyperclip.paste()
clip = raw_clip.lower()

# define all keywords to be highlighted
headers = (
    'windows',  # OS
    'mechanical_assembly',  # mech
    'linux',  # OS
    )

keywords = (
    'power_on', 'power_off', 'cycle_power',  # change power state
    'plug_the_S2LP', 'unplug_the_S2LP',  # add/remove AIC
    'plug_the_S2M2', 'unplug_the_S2M2',  # add/remove AIC
    'barcode.bat',  # prog doc
    'on-screen',  # batch file
    'assembly.pdf',  # mech doc: S2LP, J220, etc
    '.ce', '.cfg',  # config
    '.x2', '.pt', '.b3', '.d3', '.d3b', '.h8',  # prodtest
    )

# remove all double quotes
brackets = '"“”{}[]()\'' 
for c in brackets:
    clip = clip.replace(c, ' ')  # replace with space

# add underscores/dots, replace strings, or kill completely using squiggly brackets
underscore = (
    ['cycle power', 'cycle_power'],  # listed first to avoid converting 'cycle power on x' incorrectly
    ['power on', 'power_on'],
    ['power off', 'power_off'],
    ['type ce',  '.ce'],
    ['type cfg', '.cfg'],
    ['type x2',  '.x2'],
    ['type pt',  '.pt'],
    ['type b3',  '.b3'],
    ['type d3b', '.d3b'],
    ['type d3',  '.d3'],
    ['type h8',  '.h8'],
    ['perform mechanical assembly', '{redacted}'],
    ['mechanical assembly', 'mechanical_assembly'],
    ['windows pc with barcode reader', '{equipment}'],
    ['to the windows pc', '{to the equipment}'],
    ['from the windows pc', '{from the equipment}'],
    ['plug the s2lp', 'plug_the_S2LP'],
    ['unplug the s2lp', 'unplug_the_S2LP'],
    ['plug the s2m2', 'plug_the_S2M2'],
    ['unplug the s2m2', 'unplug_the_S2M2'],
    )
for u in underscore:
    clip = clip.replace(u[0], u[1])  # replace space with underscore or kill

# generate output
words = clip.split()  # lowercase, split on whitespace
print(' '.join(words) + '\nEND OF CLIPBOARD')  # debug can also do pprint.pprint
out = ''  # output string
last = 'long'  # default to last word being long
for word in words:
    if word in headers:
        out = out + '\n-- ' + word + ' --'
        last = 'long'
    elif word in keywords:
        if len(word) < 5:
            if last == 'short':
                out = out + ' ' + word  # add one leading space
            else:
                out = out + '\n   ' + word  # add leading newline and spaces
            last = 'short'
        else:
            out = out + '\n   ' + word  # add leading newline and spaces
            last = 'long'
print(out)

# write files if applicable
if 'S2LP' in out:
    with open('S2LP.log', 'w') as f:
        f.write(out + '\n')
if 'S2M2' in out:
    with open('S2M2.log', 'w') as f:
        f.write(out + '\n')

# done in batch file:
# os.system('timeout /t 60')

# EOF
