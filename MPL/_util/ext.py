import os

ext = []
ignorelist = ['gitattributes', 'gitignore']  # extensions to ignore

for p, d, f in os.walk('..\\'):  # start checking one level up
    for file in f:
        found = file.split(".")[-1]  # get last token from file name
        if found not in ext and found not in ignorelist:
            ext.append(found)  # add only if not already in list

print('Found extensions:\n')
print('\n'.join(ext))
print()

os.system("PAUSE")
