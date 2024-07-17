import os
import yaml


def GetText(s):
    try:
        with open(s + '.txt', 'r') as f:
            r = f.read()
    except:
        r = ''
    return r
#End


def GetTable():
    s = ''
    filename = 'error.html'
    try:
        with open('table.yaml', 'r') as f: 
            mytable = yaml.safe_load(f)
    except:
        mytable = {}
    for key in mytable:
        if key == 'filename':
            filename = mytable[key]
        else:
            numberletter = key.split('-')
            fn = numberletter[0] + numberletter[1].lower()  # function should use number and lowercase letter
            s = s + '    <tr style="background-color: #' + mytable[key][0] + '">\n'
            s = s + '      <td style="text-align:center">' + key + '</td>\n'
            s = s + '      <td style="text-align:center">\n'
            s = s + '        <button onclick="copyText' + fn + '()">&#10697;</button>\n'
            s = s + '        <script>function copyText' + fn + '() {navigator.clipboard.writeText("' + mytable[key][1] + '");}</script>\n'
            s = s + '      </td>\n'
            s = s + '      <td style="padding-left:15px">' + mytable[key][2] + '</td>\n'
            s = s + '    </tr>\n'
    return filename, s
# End


# start of script, get three sections of output file
a = GetText('header')
filename, b = GetTable()
c = GetText('footer')
print('Writing: ' + filename)

# write three sections to output file
with open('..\\' + filename, 'w') as f:
    f.write(a)
    f.write(b)
    f.write(c)

# pause for user input
print()
os.system("PAUSE")

# EOL
