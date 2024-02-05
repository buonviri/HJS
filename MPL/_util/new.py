# PLACE A COPY OF THIS FILE IN EACH CATEGORY SUBFOLDER

import os

# last letter of current working directly is category, assumes script was run from correct location, e.g. C:\blah\blah\blah\MPL\R
cwd = os.getcwd()[-1:]  # get last letter of current working directory, assumes you're in a single-letter category folder

# pattern of anchor file
prefix = 'EC-'
anchor = '0000'
suffix = '.txt'
pattern = prefix + anchor + cwd + suffix
fmt = "%04d"  # format string should match anchor

# blank log
logtext = ''

# blank list of part numbers
parts = []


# logging function
def log(s):
    global logtext
    logtext = logtext + s + '\n'
    print(s)
# EOFN


# add part file template with four lines of placeholder text
def AddNext(cat, part, filename):
    print()  # blank line at start, excluded from log
    log('Adding file \'' + filename + '\' to category \'' + cat + '\'')
    partpath = ''
    folderlist = []
    for digit in part[:-2]:  # each letter in the part except for the last two
        folderlist.append(digit)  # add to list of folders
    folderlist.append(part[-2:-1] + 'x')  # add final folder, e.g. '0x'
    log('  Creating/Checking folders: ' + str(folderlist))
    for folder in folderlist:
        partpath = os.path.join(partpath, folder)  # join existing path and new letter
        try:
            os.mkdir(partpath)
        except:
            print('  Path exists: ' + partpath)  # print instead of log, don't need permanent record
    newfile = os.path.join(partpath, filename)
    with open (newfile, 'w') as f:
        f.write('manufacturer\npartnumber\ndescription\ndatasheet\n')
    log('Wrote \'' + filename + '\'')
    print()  # blank line at end, excluded from log
    return newfile
# EOFN


# ----------- START OF SCRIPT -----------

# pattern confirmation
print('Looking in folder \'' + cwd + '\' for:\n' + pattern + ' ...\n')

# find all files
for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        # check if length, prefix, and suffix are correct
        if len(filename) == len(pattern) and filename.startswith(prefix) and filename.endswith(suffix):
            print(filename)  # do not log, just print
            part = filename[len(prefix):-len(suffix)]  # remove prefix and suffix
            parts.append(part)  # add to list

# sort list
parts.sort()

# add one to last number in list
last = parts[-1][:-1]  # last part in list with category letter (last letter) removed
next = int(last) + 1  # add one to int version of number to get next available
nextstr = fmt % (next)  # format to match filename
nextfile = prefix + nextstr + cwd + suffix  # assemble filename of next part
newfile = AddNext(cwd, nextstr, nextfile)  # add the file and any necessary folders

# update log file
with open ('new.log', 'a') as f:
    f.write(logtext)

# pause for user input
os.system("PAUSE")

# launch in editor after unpausing
os.startfile(newfile)

# EOF
