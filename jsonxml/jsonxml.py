import os
import re
import pprint

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
        print('  Done\n')
# end of main loop

if clipboard:
    pyperclip.copy(formatted)
    print('Info written to clipboard')

print()
os.system("PAUSE")
# EOF
