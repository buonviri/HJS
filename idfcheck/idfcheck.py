import os
import re
import pprint
import pyperclip

# board-specific hole locations:
info = {
    '3.2000':  # diameter is dictionary key
        {'start of': 'hole locations for 3.2000',
         'XXX.XXXX YYY.YYYY': ' X) this is the expected format',
         ' 36.1000  20.7500': ' B) HS-BL-A',
         ' 76.1000  20.7500': ' B) HS-BR-A',
         ' 36.1000  60.7500': ' B) HS-TL-A',
         ' 76.1000  60.7500': ' B) HS-TR-A',
         '103.9000  20.7500': ' B) HS-BL-B',
         '143.9000  20.7500': ' B) HS-BR-B',
         '103.9000  60.7500': ' B) HS-TL-B',
         '143.9000  60.7500': ' B) HS-TR-B',
         'end of': 'hole locations for 3.2000',
        },
    '3.1800':  # diameter is dictionary key
        {'start of': 'hole locations for 3.1800',
         'XXX.XXXX YYY.YYYY': ' X) this is the expected format',
         '  7.5000   9.3500': ' A) Lower LP Hole, Spec',
         '  7.5000  63.2500': ' A) Upper LP Hole, Spec',
         'end of': 'hole locations for 3.1800',
        },
    '0.6500':  # diameter is dictionary key
        {'start of': 'hole locations for 0.6500',
         'XXX.XXXX YYY.YYYY': ' X) this is the expected format',
         'end of': 'hole locations for 0.6500',
        },
    '0.5999':  # diameter is dictionary key
        {'start of': 'hole locations for 0.5999',
         'XXX.XXXX YYY.YYYY': ' X) this is the expected format',
         'end of': 'hole locations for 0.5999',
        },
    }

# length and width variants
lengths = {'167.6500': 'Half Length', '167.5000': 'Half Length',  # max/nom
           '168.3000': 'Half Length (+USB)',  # nom card with USB
           '253.8700': '3/4 Length',  # allows for tolerance
           '254.0000': '3/4 Length',  # max
           '266.7000': 'GPU Length',
           '267.2000': 'GPU Length with 0.5mm panel extension',
           '267.5000': 'GPU Length with 0.8mm panel extension',
           '312.0000': 'Full Length', '311.8700': 'Full Length'}  #max/nom
heights = {'111.1500': 'Standard Height (FH)',
           '42.1500': 'Conversion Kit',
           '68.9000': 'Low Profile (HH)', '68.7500': 'Low Profile (HH)'}  #max/nom

bdf = '.bdf'  # file extension to check for (bdf/brd/etc)
ldf = '.ldf'  # file extension to check for (ldf/pro/etc)
fmt = "%.4f"  # set decimal places for numeric output (e.g. x.xxxx)
sections = (".HEADER", ".BOARD_OUTLINE", ".DRILLED_HOLES", ".PLACEMENT", ".ELECTRICAL", ".MECHANICAL")
endsections = (".END_HEADER", ".END_BOARD_OUTLINE", ".END_DRILLED_HOLES", ".END_PLACEMENT", ".END_ELECTRICAL", ".END_MECHANICAL")
section = ''
corners = {}
corner_count = 0
xmin = +9999.9999
xmax = -9999.9999
ymin = +9999.9999
ymax = -9999.9999
clip = {}
library = {}
good = 0
bad = 0
libcount = 0

def get_tokens(x):
    return [p for p in
            re.split("( |\\\".*?\\\"|'.*?')", x.strip())
            if p.strip()]


for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        myfile = os.path.join(dirname, filename)
        holes = {}
        if filename.endswith(bdf):  # only initialize the dictionary for bdf
            for k in info:
                holes[k] = []  # create a blank list for each diameter that is listed in info
        if filename.endswith(bdf) or filename.endswith(ldf):
            with open(myfile) as f:
                print("\nFile: " + myfile)
                for line in f:
                    tokenlist = get_tokens(line)
                    if tokenlist[0] in sections:
                        section = tokenlist[0]
                    elif tokenlist[0] in endsections:
                        section = ''
                    elif section == ".BOARD_OUTLINE":
                        if len(tokenlist) == 4:  # skips the thickness line
                            if tokenlist[0] == '0':  # skips cutouts which have loop ID of 1 or higher
                                corners[corner_count] = (tokenlist[0],tokenlist[1],tokenlist[2],tokenlist[3])
                                corner_count = corner_count + 1
                    elif section == ".DRILLED_HOLES":
                        if tokenlist[0] in holes:  # check if hole diameter is a key in the dictionary
                            holes[tokenlist[0]].append([tokenlist[1],tokenlist[2]])  # append list of XY to dia entry
                    elif section == ".PLACEMENT":
                        if len(tokenlist) == 3:  # first line of component entry
                            refdes = tokenlist[2]  # save refdes
                            libkey = tokenlist[0] + ' (' + tokenlist[1] + ')'  # key format is 'footprint (partname)'
                        elif len(tokenlist) == 6:  # second line of component entry
                            if tokenlist[2] != '0.0000':  # assumes 4dp precision, could change to list of valid strings
                                print(tokenlist[2] + ' offset found for ' + refdes)
                            clip[refdes] = [tokenlist[2],libkey]  # create new list for key=refdes with Z offset and libkey
                        else:  # invalid token count
                            print(tokenlist)
                    elif section == ".ELECTRICAL" or section == ".MECHANICAL":
                        if tokenlist[2] == 'MM':  # could add 'THOU' to allow imperial files
                            libkey = tokenlist[0] + ' (' + tokenlist[1] + ')'  # key format is 'footprint (partname)'
                            library[libkey] = [tokenlist[3],[],[]]  # height is first entry in list followed by X and Y lists
                            libcount = libcount + 1
                        else:  # not the first line, so assume vertex
                            library[libkey][1].append(float(tokenlist[1]))  # add x as float
                            library[libkey][2].append(float(tokenlist[2]))  # add y as float

# create clipboard string
s = ''
invalid_corners = []
for k in clip:
    try:
        offset = clip[k][0]  # Z offset
        part = clip[k][1]  # footprint (partname) string
        zxy = library[part]  # list containing z-x-y info
        x = fmt % (max(zxy[1]) - min(zxy[1]))  # calc size in X
        y = fmt % (max(zxy[2]) - min(zxy[2]))  # calc size in Y
        s = s + '\t'.join([k, offset, zxy[0], x, y, part]) + '\n'  # refdes, zoffset, z, x, y, partinfo
        good = good + 1
        if len(zxy[1]) != 5 or len(zxy[2]) != 5:  # should five X and five Y
            if clip[k][1] not in invalid_corners:
                print('Invalid number of corners found for ' + k + ' (example refdes)')
                print('   ' + clip[k][1])
                invalid_corners.append(clip[k][1])  # save to list so it doesn't print again
    except:  # failed dictionary lookup, insert negative one as placeholder
        s = s + clip[k][0] + '\t' + clip[k][1] + '\t' + '-1.0' + '\n'
        bad = bad + 1
pyperclip.copy(s)
print('\nCopied info to clipboard. Good lines = ' + str(good) + '. Bad lines = ' + str(bad) + '.')
print('Libcount = ' + str(libcount))

s = []
for dia in holes:
    for xy in holes[dia]:
        key = xy[0].rjust(8) + ' ' + xy[1].rjust(8)
        try:
            hole_detail = info[dia][key]
        except:
            hole_detail = "   "  # three blanks to align with 'X) '
        if float(dia) > .4999 or hole_detail != '   ':  # only print larger holes, UNLESS it's a named hole
            s.append('\nHole' + hole_detail + ' (' + xy[0] + ' ' + xy[1] + ')')
s.sort()
print(*s)

print('')
for k in corners:
    x = float(corners[k][1])
    y = float(corners[k][2])
    if x < xmin:
        xmin = x
    if y < ymin:
        ymin = y
    if x > xmax:
        xmax = x
    if y > ymax:
        ymax = y
print('Bottom Left: (' + fmt % xmin + ' ' + fmt % ymin + ')')
print('  Top Right: (' + fmt % xmax + ' ' + fmt % ymax + ')')
sizex = fmt % (xmax-xmin)
sizey = fmt % (ymax-ymin)

try:
    length = lengths[sizex]
except:
    length = 'Unknown Length'  # PCIe Length
try:
    height = heights[sizey]
except:
    height = 'Unknown Height'  # PCIe Height
print('       Size: (' + sizex + ' ' + sizey + '), ' + height + ', ' + length)

print('')
os.system("PAUSE")
# EOF
