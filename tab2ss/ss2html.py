import os
import ast

with open('tab2ss.list', 'r') as f:  # open stored list from subfolder
    ss = ast.literal_eval(f.read())  # convert to spreadsheet

html = ''
html = html + '<!DOCTYPE html>\n'
html = html + '<HTML lang="en">\n'
html = html + '<HEAD>\n'
html = html + '  <META charset="utf-8">\n'
html = html + '  <STYLE>table, th, td {border: 1px solid #DDDDDD; border-collapse: collapse; word-wrap: break-word; table-layout: fixed;}</STYLE>\n'
html = html + '  <STYLE>body {margin: 25px; color: #DDDDDD; background-color: #222222;}</STYLE>\n'
html = html + '  <TITLE>BOM</TITLE>\n'
html = html + '</HEAD>\n'
html = html + '<BODY>\n'
# html = html + 'Bill of Materials<BR><BR>\n'
html = html + '  <TABLE style="width:100%">\n'
rows = len(ss)  # get row count
for i in range(rows):
    html = html + '    <tr>\n'
    row = ss[i]
    colcount = len(row)
    if i == 0 and colcount == 6 and row[0] == 'ECPN':  # BOM
        width = ['<td style="width:10%">', '<td style="width:5%">', '<td>', '<td style="width:15%">', '<td style="width:15%">', '<td style="width:20%">']
    elif i == 0 and colcount == 6 and row[0] == 'RefDes':  # alternate BOM?
        width = ['<td style="width:10%">', '<td style="width:10%">', '<td style="width:15%">', '<td style="width:15%">', '<td style="width:20%">', '<td>']
    elif i == 0 and colcount == 4 and row[0] == 'ECPN':  # inventory output from ECPL gsheet
        width = ['<td style="width:15%">', '<td style="width:15%">', '<td style="width:35%">', '<td>']
    else:
        width = ['<td>'] * colcount
    if i == 0:
        height = ['<H2>', '</H2>']
    else:
        height = ['', '']
    for j in range(colcount):
        cell = row[j]
        html = html + '      ' + width[j] + height[0] + cell + height[1] + '</td>\n'
    html = html + '    </tr>\n'
html = html + '  </TABLE>\n'
html = html + '</BODY>\n'
html = html + '</HTML>\n'

outfile = 'ss.html'
with open(outfile, 'w') as f:
    f.write(html + '\n')

print('Wrote: ' + outfile)
print()
os.system("PAUSE")
# End
