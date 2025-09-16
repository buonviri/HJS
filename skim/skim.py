import os
import pprint
import pyperclip

raw_clip = pyperclip.paste()
clip = raw_clip.lower()

# define all keywords to be highlighted
headers = (
    'windows', 'linux',  # OS
    'mechanical_assembly',  # mech
    # 'final_test',  # test header removed because it also contains 'linux'
    )

keywords = (
    'power_on', 'power_off', 'cycle_power',  # change power state
    'plug_the_S2LP', 'unplug_the_S2LP',  # add/remove
    'barcode.bat',  # prog doc
    'assembly.pdf',  # mech doc
    '.ce', '.cfg',  # config
    '.x2', '.pt', '.b3', '.d3', '.d3b', '.h8',  # prodtest
    )

# remove all double quotes
double_quotes = '"“”' 
for c in double_quotes:
    clip = clip.replace(c, '')  # delete completely

# separate keywords from delimiters
add_space = "{}[]()'"  # this string is double-quoted since those are aleady gone
for a in add_space:
    clip = clip.replace(a, ' ' + a + ' ')  # replace each char with that same char plus leading/trailing spce

# add underscores or kill completely using squiggly brackets
underscore = (
    ['cycle power', 'cycle_power'],  # listed first to avoid converting 'cycle power on x' incorrectly
    ['power on', 'power_on'],
    ['power off', 'power_off'],
    ['final test', 'final_test'],
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
    )
for u in underscore:
    clip = clip.replace(u[0], u[1])  # replace space with underscore or kill

# generate output
words = clip.split()  # lowercase, split on whitespace
print(' '.join(words) + '\nEND OF CLIPBOARD\n')  # debug can also do pprint.pprint
for word in words:
    if word in headers:
        print('** ' + word + ' **')
    elif word in keywords:
        print(' ' + word)

# done in batch file:
# os.system('timeout /t 60')

# EOF
