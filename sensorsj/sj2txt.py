import ast
import os

# function copied from recolor.py in ballmap:
def GetFiles(where, pattern, type):
# where can be here or walk
# pattern is a string
# type can be start, end, in, or exact
    flist = []  # blank list
    if where == 'here':
        for fname in os.listdir():
            if type == 'start' and fname.startswith(pattern):
                flist.append(fname)
            elif type == 'end' and fname.endswith(pattern):
                flist.append(fname)
            elif type == 'in' and pattern in fname:
                flist.append(fname)
            elif type == 'exact' and fname == pattern:
                flist.append(fname)
    return flist
# End


good = ''
keycombos = [  # devicename|sensorprefix|valueprefix
    'nct6798-isa-02a0|fan|fan',
    'nct6798-isa-02a0|CPUTIN|temp',
    'coretemp-isa-0000|Core|temp',
    ]
filelist = GetFiles('here', '.sj', 'end')
for filename in filelist:
    print(filename)
    with open(filename, 'r') as f:
        wholefile = f.read()
        sjdict = ast.literal_eval(wholefile)
        for i in sjdict:
            for j in sjdict[i]:
                if type(sjdict[i][j]) is str:
                    pass  # was used to generate keys.txt: print(str(i) + '|' + str(j))
                elif type(sjdict[i][j]) is dict:
                    for k in sjdict[i][j]:
                        pass  # was used to generate keys.txt: print(str(i) + '|' + str(j) + '|' + str(k))
                else:
                    print('Type mismatch error (LOL)')
    # print('Checking for combos...')
    for keycombo in keycombos:
        keylist = keycombo.split('|')
        firstkey = keylist[0]
        try:
            device = sjdict[firstkey]
            for secondkey in device:
                if secondkey.startswith(keylist[1]):
                    sensor = sjdict[firstkey][secondkey]
                    for thirdkey in sensor:
                        if thirdkey.startswith(keylist[2]) and thirdkey.endswith('input'):  # only keep the inputs, not min/max/beep/alarm/etc
                            sensorvalue = str(sjdict[firstkey][secondkey][thirdkey])
                            good = good + sensorvalue
                            good = good + ' (' + filename + ': ' + firstkey + '|' + secondkey + '|' + thirdkey + ')\n'
        except:
            pass

print('\nFound sensors:')
print(good)

os.system('PAUSE')

# EOF
