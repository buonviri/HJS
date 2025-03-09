# generates all cfg edit strings and scripts
import os
import ast

# info
prefix = '@python.exe C:\\EdgeCortix\\HJS\\statlog\\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+'
suffix = '+C-fast\n'  # removed for better all batch file performance: @timeout 60\n
plinux = 'python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+'
slinux = '+C-fast'
foo = {}  # empty dict to store imported file info
files = {  # py extension allows auto-color, key is desc of range, val is filename
    'S2LP-D16 v1.5 for BMC 1.0.x': '.52979.14.28.py',
    'S2LP-S16 v1.5 for BMC 1.0.x': '.52980.1.5.py',  # also contains dual -> single overrides
    'S2LP-S16 v1.5 for BMC 1.1.x': '.52980.6.13.py',
    'S2M2-S16 v1.5 for BMC 1.0.x': '.10014.1.42.py',
    'S2M2-S16 v1.5 for BMC 1.1.x-feb': '.10015.1.28.py',
    'S2M2-S16 v1.5 for BMC 1.1.x-mar': '.10015.52.255.py',
    }

# end of info, start of functions
def checkdir(dirname):
    try:
        os.mkdir(dirname)  # attempt to add folder
        print('| ' + dirname + ' created ', end='')
    except:
        print('| ' + dirname + ' exists ', end='')
# End
def bracketreplace(s):
    s = s.replace('[DASH]', '-')
    s = s.replace('[DOT]', '.')
    return s
# End

# end of functions, start of script
for key in files:  # check every key
    with open(files[key], 'r') as f:  # open filename of key
        val = ast.literal_eval(f.read())  # read contents into val
        foo[key] = val

count = 0
for config in foo:
    count = count + 1
    print('\n' + str(count) + ') Generating files for: ' + config)
    cfg = foo[config]  # this cfg's dictionary
    for rawlotcode in cfg['lotcodes']:
        lotcode = rawlotcode.strip('+')  # plus sign may be used to add to lotcode
        print('   Folders ', end='')  # prefix, indent 3
        checkdir(lotcode)  # create folder if missing
        checkdir(lotcode + '\\linux')  # create folder if missing
        checkdir(lotcode + '\\plain_text')  # create folder if missing
        print()  # suffix
        start = ''
        end = ''
        for i in range(cfg['lotcodes'][rawlotcode][0], cfg['lotcodes'][rawlotcode][1] + 1):
            sn = '%03d' % i
            fname = 'cfg-edit-' + lotcode + '-PAC' + sn
            if len(start) == 0:
                start = '     ' + fname  # indent 5
            else:
                end = ' thru ' + fname
            commands = []
            for parameter in cfg['parameters']:
                # print('    ' + parameter + '=' + cfg['parameters'][parameter])
                commands.append(cfg['parameters'][parameter].replace('[LOTCODE]', lotcode).replace('[SERIALNUMBER]', sn))
            with open('.\\' + lotcode + '\\' + fname  + '.bat', 'w') as f:
                f.write(prefix + '+'.join(commands) + suffix)
            with open('.\\' + lotcode + '\\linux\\' + lotcode + sn + '.sh', 'w') as f:
                f.write(plinux + '+'.join(commands) + slinux)
            with open('.\\' + lotcode + '\\plain_text\\' + lotcode + sn + '.txt', 'w') as f:
                f.write(prefix + '\n\n' + bracketreplace('\n'.join(commands)) + '\n\n' + suffix)  # extra newlines
        print(start + end)
# EOF

# @python.exe C:\EdgeCortix\HJS\statlog\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+S2M2+S16NFN+10014[DASH]PAC001+10014001+1+5+0+2[DOT]01+20250117+20250123+1+0+2+800+1+0+550+2+0+1+99+95+85+1+1+C-fast
# @timeout 60
