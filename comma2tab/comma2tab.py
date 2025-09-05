import csv
import pyperclip


def GetTokens(x):  # modified to split on comma
    return [ '{}'.format(x) for x in list(csv.reader([x], delimiter=',', quotechar='"'))[0] ]
# end of GetTokens()


# start of script
txtreplace = {
    'CPU Core #1': 'CPU#1',
    'HX1000i Power In'  : 'In (W)',
    'HX1000i Power Out' : 'Out (W)',
    'HX1000i 12V Power' : 'P12V (W)',
    'HX1000i 5V Power'  : 'P5V0 (W)',
    'HX1000i 3.3V Power': 'P3V3 (W)',
    }  # end of txtreplace

cells = pyperclip.paste()  # get tab data from clipboard
lines = cells.split('\n')
out = ''
for line in lines:
    newline = GetTokens(line)
    out = out + '\t'.join(newline) + '\n'

# replace strings
for k in txtreplace:
    out = out.replace(k, txtreplace[k])  # replace string

# place on clipboard
pyperclip.copy(out)  # place result on clipboard

# EOF
