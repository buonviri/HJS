# generates all cfg edit strings and scripts
import os

# info
prefix = '@python.exe C:\\EdgeCortix\\HJS\\statlog\\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+'
suffix = '+C-fast\n@timeout 60\n'
foo = {
    'S2M2 v1.5 for BMC 1.0.x':  {
        'lotcodes': {
            '10014': (1,42),
            #  debug: '52461': (1,2),
        },
        'parameters': {
            'name': 'S2M2',
            'var': 'S16NFN',
            'sntxt': '[LOTCODE][DASH]PAC[SERIALNUMBER]',
            'sndec': '[LOTCODE][SERIALNUMBER]',
            'rev': '1',
            'ecn': '5',
            'ddr': '0',
            'sak': '2[DOT]01',
            'mfgdate': '20250117',
            'ecndate': '20250123',
            'p0v8': '1',
            'p3v3': '0',
            'cblimit': '2',
            'pll': '800',
            'pcie': '1',
            'pmode': '0',
            'vcore': '550',
            'cba': '2',
            'cbb': '0',
            'cbd': '1',
            'bmctemp': '99',
            'saktemp': '95',
            'boardtemp': '85',
            'pwren': '1',
            'saken': '1',
        },
    }
}

# end of info, start of functions


def checkdir(dirname):
    try:
        os.mkdir(dirname)  # attempt to add folder
        print('  Created folder: ' + dirname)
    except:
        print('  Folder exists: ' + dirname)
# End


# end of functions, start of script

for config in foo:
    print('Generating files for: ' + config)
    cfg = foo[config]  # this cfg's dictionary
    for lotcode in cfg['lotcodes']:
        checkdir(lotcode)  # create folder if missing
        start = ''
        for i in range(cfg['lotcodes'][lotcode][0], cfg['lotcodes'][lotcode][1] + 1):
            sn = '%03d' % i
            fname = 'cfg-edit-' + lotcode + '-PAC' + sn + '.bat'
            if len(start) == 0:
                start = '    ' + fname
            end = ' thru ' + fname
            commands = []
            for parameter in cfg['parameters']:
                # print('    ' + parameter + '=' + cfg['parameters'][parameter])
                commands.append(cfg['parameters'][parameter].replace('[LOTCODE]', lotcode).replace('[SERIALNUMBER]', sn))
            with open('.\\' + lotcode + '\\' + fname, 'w') as f:
                f.write(prefix + '+'.join(commands) + suffix)
        print(start + end)
# EOF

# @python.exe C:\EdgeCortix\HJS\statlog\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+S2M2+S16NFN+10014[DASH]PAC001+10014001+1+5+0+2[DOT]01+20250117+20250123+1+0+2+800+1+0+550+2+0+1+99+95+85+1+1+C-fast
# @timeout 60
