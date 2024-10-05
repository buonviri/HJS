import os


def fix(info):
    new = ''
    for line in info:
        nospaces = line.replace(' ','')
        if '=PRODUCT(' in nospaces:
            print(nospaces)
        new = new + line
# End


# start of script
print()  # blank line to separate from prompt
for filename in os.listdir():  # only look in current folder
    n = filename.lower()  # only used for checking extension
    if n.endswith('.step') or n.endswith('.stp'):
        name = filename + ' temp.txt'  # remove and overwrite original file later
        print('Writing: ' + name)
        with open(filename, 'r') as f:
            info = f.readlines()  # read entire file and pass as a list
        new = fix(info)
        with open(name, 'w') as f:
            f.write(''.join(info))
# end of main loop

print()
# os.system("PAUSE")
# EOF