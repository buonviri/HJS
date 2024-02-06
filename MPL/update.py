import os
import pprint

# project name, pick whatever you want, do not ever change it!
project = 'ECPL'

# prefix string, inserted in front of all part numbers
prefix = 'EC-'

# list of part number sub folders to be created for any new category
subfolders = ['0','0','0x']

# relative path from last folder in list back to top level
up = '../../../../'

# anchor file is the first part number in any category
anchor = '0000'

# recommended extension is .txt, alt is all caps, must be same length
extension = '.txt'
alt_extension = '.TXT'

#  name length is prefix + anchor + 1 (category) + extension
name_length = len(prefix) + len(anchor) + 1 + len(extension)

# this list of categories contains tuples with category letter and category name
# the order of parts in the html file will match the order in this list
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

# dictionary for exporting
info = {}

# logging function
def log(s):
    global logtext
    logtext = logtext + s + '\n'


# add category
def AddCategory(letter, name):
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


# get info from file
def GetInfo(dirname, filename):
    with open (os.path.join(dirname,filename), 'r') as f:
        lines = [line.strip() for line in f]  # generates a list of the lines without whitespace
    return [dirname,] + lines


# HTML strings
BodyHTML = """<BODY BGCOLOR="#222222" TEXT="#DDDDDD" LINK="#0000FF" VLINK="0099FF" ALINK="#FF0000">\n\n"""
StyleHTML = """  <p style="margin-left: 25px; margin-top: 25px;">\n"""
TitleStartHTML = """    <H2>"""
TitleEndHTML = """<H2>\n"""
EndHTML = """  </p>\n\n</BODY>\n"""


def GenerateHTML(filename, title):
    mainhtml = BodyHTML + StyleHTML + TitleStartHTML + title + TitleEndHTML
    for c in categories:  # iterate over categories for both main and part HTML files 
        cat_letter = c[0]  # zeroth string in tuple is the letter
        mainhtml = mainhtml + '    <br><H2>' + info[cat_letter]['name'] + ' (' + cat_letter + ')</H2>\n'
        parts = info[cat_letter]['parts']  # get list of parts for this category
        for part in parts:  # iterate over each part in the current category
            partinfo = info[cat_letter][part]  # list of strings for each part
            partinfo = partinfo + ['', '', '', '',]  # add four blank strings just in case not enough are provided
            parthtml = BodyHTML + StyleHTML
            parthtml = parthtml + '    ' + partinfo[1] + ' ' + partinfo[2] + '<br>' + partinfo[3] + '<br>\n'  # add mfg info
            parthtml = parthtml + '    ' + part + '<br><br>\n'  # add mpl info
            link_to_part = part + '.html'  # defaults to the html file, but may get replaced with [direct] link
            for rawline in partinfo[4:]:  # if there are more than four lines, the rest are links
                line = rawline.strip()  # remove spaces
                if len(line) < 2:  # lines with only one character aren't valid, replace with blank
                    line = ''  # won't generate standard link below
                elif line[1] in r'\/':  # if second char is slash (uses raw string as list)
                    line = up + line[0] + '/' + line[2:]  # replace path with proper one
                if line.lower().startswith('[direct]'):  # check if line starts with the direct tag, case-insensitive
                    page = ''  # default to not having a page ref
                    directpage = line.split(' ')  # space separates tag and page number
                    if len(directpage) == 2:  # direct tag plus a page number equals two list items
                        page = '#page=' + directpage[1]  # add the page indicator plus the page number
                    link_to_part = lastlink + page  # append page, might be empty string
                    line = ''  # won't generate standard link below
                if ' -> ' in line:  # look for arrow to indicate alternate text
                    linkandtext = line.split(' -> ')  # split into link and text
                    link = linkandtext[0]
                    text = linkandtext[1]
                else:
                    link = line  # whole line is also link, may include page number
                    text = line.split('.')[-1]  # last item in list is extension, which is displayed text by default
                    if '#' in text:  # if there's a # in the extension, the link includes a page number or other html feature
                        text = text.split('#')[0]  # split on # and take the first token only, e.g. 'pdf#page=8' becomes 'pdf' again
                if link is not '':  # don't add a link if it's blank
                    parthtml = parthtml + '    <A HREF="' + link + '">' + text + '</a><br>\n'  # write link and text as anchor
                lastlink = link
                lasttext = text  # currently unused
            parthtml = parthtml + EndHTML
            with open (os.path.join(partinfo[0], part + '.html'), 'w') as f:
                f.write(parthtml)
            if part == prefix + anchor + cat_letter:  # look for anchors
                print('Found anchor: ' + part)
            else:  # non-anchors get added to HTML
                mainhtml = mainhtml + '    ' + partinfo[1] + ' ' + partinfo[2] + '<br>' + partinfo[3] + '<br>\n'
                mainhtml = mainhtml + '    <A HREF="./' + partinfo[0].replace('\\','/') + '/' + link_to_part + '">' + part + '</A><br><br>\n'
    mainhtml = mainhtml + EndHTML
    with open (filename, 'w') as f:
        f.write(mainhtml)
    

# ----------- START OF SCRIPT -----------

# iterate over all the categories
for c in categories:
    parts = []  # blank list for storing part numbers to be sorted later
    cat_letter = c[0]
    cat_name = c[1]
    info[cat_letter] = {}  # add category to dict
    info[cat_letter]['name'] = cat_name  # add name to dict
    if not os.path.isdir(cat_letter):  # check if letter is missing as folder
        AddCategory(cat_letter, cat_name)  # add folder
    else:
        for dirname, dirnames, filenames in os.walk(cat_letter):  # get info from category
            for filename in filenames:
                # check if length and extension are correct
                if len(filename) == name_length and filename[-len(extension):] in [extension, alt_extension]:
                    part = filename[0:-len(extension)]  # remove extension
                    info[cat_letter][part] = GetInfo(dirname, filename)  # add info from file to dict
                    parts.append(part)  # add part to temporary list
    info[cat_letter]['parts'] = sorted(parts)

# write html
GenerateHTML(project + '.html', 'Master Parts List')

# write dict
with open (project + '.dict', 'w') as f:
    f.write(pprint.pformat(info, indent=2))

# append log file
with open (project + '.log', 'a') as f:
    f.write(logtext)

# EOF
