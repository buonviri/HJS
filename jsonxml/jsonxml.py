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


def display_all_levels(element, level=0):

    printme = 0
    if element.text and "R111" in element.text:
        printme = 1
    if element.attrib:
        for a in element.attrib:
            if "R111" in a:
                printme = 1
    if printme:
        # Print the element tag with appropriate indentation to show its level
        print(' ' * level + element.tag.split('}')[-1], end='')
    
        # Optionally, print attributes and text
        if element.attrib:
            print(f" (attributes: {element.attrib})", end='')
        if element.text and element.text.strip():
            print(f" (text: {element.text.strip()})", end='')
        print()

    # Recurse through all child elements
    for child in element:
        display_all_levels(child, level + 1)
# end


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
        tree = ET.parse(filename)
        root = tree.getroot()
        display_all_levels(root)
        info = {'comps': {}, 'nets': {}}
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
