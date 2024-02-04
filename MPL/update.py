import os

# project name, pick whatever you want, do not ever change it!
project = 'ECPL'

# prefix string, inserted in front of all part numbers
prefix = 'EC-'

# list of part number sub folders to be created for any new category
subfolders = ['0','0','0x']

# anchor file is the first part number in any category
anchor = '0000'

# recommended extension is .txt, alt is all caps, must be same length
extension = '.txt'
alt_extension = '.TXT'

#  name length is prefix + anchor + 1 (category) + extension
name_length = len(prefix) + len(anchor) + 1 + len(extension)

# this list of categories contains tuples with category letter and category name
categories =[
    ('A','Assemblies',),
    ('B','Sub-Assemblies',),
    ('C','Capacitors',),
    ('L','Inductors',),
    ('M','Mechanical',),
    ('R','Resistors',),
    ('U','ICs',),
    ('W','Documents',),
    ]  # end of categories

# blank log
logtext = ''


# logging function
def log(s):
    global logtext
    logtext = logtext + s + '\n'


# add category
def add(letter, name):
    os.mkdir(letter)  # add folder
    log('Added folder: ' + cat_letter + ' (' + cat_name + ')')
    current_folder = cat_letter  # initialize
    for sub in subfolders:  # loop through list of subfolders and create each one
        current_folder = os.path.join(current_folder,sub)
        os.mkdir(current_folder)
        log('Added folder: ' + current_folder)
    anchor_filename = prefix + anchor + cat_letter + extension  # create file name for anchor
    with open (os.path.join(current_folder, anchor_filename), 'w') as f:
        f.write(project + '\n' + cat_name + '\n' + anchor_filename + ' is reserved as the category anchor\n')
    log('Added file: ' + anchor_filename)


# iterate over all the categories
for c in categories:
    cat_letter = c[0]
    cat_name = c[1]
    if not os.path.isdir(cat_letter):  # check if letter is missing as folder
        add(cat_letter, cat_name)  # add folder
    else:
        for dirname, dirnames, filenames in os.walk(cat_letter):  # get info from category
            for filename in filenames:
                # check if length and extension are correct
                if len(filename) == name_length and filename[-len(extension):] in [extension, alt_extension]:
                    log('Found: ' + filename)

# update log file
with open (project + '.log', 'a') as f:
    f.write(logtext)
