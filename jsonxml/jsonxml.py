import os
import re
import pprint
import xml.etree.ElementTree as ET

# generates JSON file and clipboard:
#   header included
#   components section
#   nets section

if os.name == 'nt':  # clipboard generally only works in windows
    try:
        import pyperclip
        clipboard = True
    except:
        print('\nRequires pyperclip. Use: pip install pyperclip')
        clipboard = False


def convert(lines):
    info = {'comps': {}, 'nets': {}}  # blank dict for storing all netlist info
    for line in lines:
        if 'CommonCorePart' in line and 'Reference' in line:  # both words should appear on BOM lines
            # '<CommonCorePart OccId="28169" PartNumber="" Reference="R111"/>'
            tokens = line.split('=')  # split on equality sign
            next = 'nothing'
            for token in tokens:
                if next == 'Reference':
                    next = 'nothing'
                    refdes = token.split('"')[1]
                    try:  # append
                        info['comps'][refdes].append(line.strip())
                    except:  # doesn't exist
                        info['comps'][refdes] = [line.strip(),]  # new list
                if token.endswith('OccId'):
                    next = 'OccId'
                if token.endswith('PartNumber'):
                    next = 'PartNumber'
                if token.endswith('Reference'):
                    next = 'Reference'
    return info
# end of convert()


# start of script
print()  # blank line to separate from prompt
for filename in os.listdir():  # only look in current folder
    n = filename.lower()  # only used for checking extension
    if n.endswith('.xml'):
        name = filename + ' converted to.dict'
        print('Writing: ' + name)
        with open(filename, 'r') as f:
            info = convert(f.readlines())  # read entire file and pass as a list
        with open(name, 'w') as f:
            formatted = pprint.pformat(info, indent=2, width=200)
            f.write(formatted + '\n')  # write using pformat
        print('  BOM Count: ' + str(len(info['comps'])) + ' (ABC Check)')
        print('  Done\n')
# end of main loop

if clipboard:
    pyperclip.copy(formatted)
    print('Info written to clipboard')

print()
os.system("PAUSE")
# EOF
