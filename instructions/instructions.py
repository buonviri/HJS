import yaml
htmlname = '..\\EC-0012W Instructions.html'  # should be read from yaml

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
    try:
        with open('table.yaml', 'r') as f: 
            mytable = yaml.safe_load(f)
    except:
        mytable = {}
    for key in mytable:
        numberletter = key.split('-')
        fn = numberletter[0] + numberletter[1].lower()  # function should use number and lowercase letter
        s = s + '    <tr style="background-color: #' + mytable[key][0] + '">\n'
        s = s + '      <td>' + key + '</td>\n'
        s = s + '      <td>\n'
        s = s + '        <button onclick="copyText' + fn + '()">&#10697;</button>\n'
        s = s + '        <script>function copyText' + fn + '() {navigator.clipboard.writeText("' + mytable[key][1] + '");}</script>\n'
        s = s + '      </td>\n'
        s = s + '      <td>' + mytable[key][2] + '</td>\n'
        s = s + '    </tr>\n'
    return s
# End


# start of script
with open(htmlname, 'w') as f:
    f.write(GetText('header'))
    f.write(GetTable())
    f.write(GetText('footer'))
# EOL
