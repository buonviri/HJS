import csv
import pyperclip


def GetTokens(x):  # modified to split on comma
    return [ '{}'.format(x) for x in list(csv.reader([x], delimiter=',', quotechar='"'))[0] ]
# end of GetTokens()


# start of script
cells = pyperclip.paste()  # get tab data from clipboard
lines = cells.split('\n')
out = ''
for line in lines:
    newline = GetTokens(line)
    out = out + '\t'.join(newline) + '\n'
pyperclip.copy(out)  # place result on clipboard

# EOF
