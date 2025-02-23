# formatted telemetry

with open('telem.info', 'rb') as f:
    telem = f.read()

s = ''
for c in telem:
    if c>31 and c<127 and c!=32:  # in range but not space or tab
        s = s + chr(c)
    elif c == 10 or c == 13:  # replace newline with comma
        s = s + ','
s = s.strip(',')
telemetry = s.split(',')

filtered = []
for t in telemetry:
    if t.startswith('W_P3V3'):
    	filtered.append('P_P3V3')
    else:
        filtered.append(t)

header = ''
data = ''
for i in range(5):  # only works for S2M2
    header = header + filtered[i].ljust(10)
    floatdata = float(filtered[i+5])
    stringdata = '%.2lf' % floatdata
    data = data + stringdata.ljust(10)
header = header.replace('P3V3', '3V3 ')  # remove unnecessary P
print(header)
print(data)

# EOF
