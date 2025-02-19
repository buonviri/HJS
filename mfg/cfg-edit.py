# generates all cfg edit strings and scripts
import os

# info
prefix = '@python.exe C:\\EdgeCortix\\HJS\\statlog\\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+'
suffix = '+C-fast\n@timeout 60\n'
plinux = 'python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+'
slinux = '+C-fast'
foo = {
    'S2M2-S16 v1.5 for BMC 1.0.x':  {
        'lotcodes': {
            '10014': (1,42),
            #  debug: '52461': (1,2),
        },
        'parameters': {
            'name': 'S2M2',
            'var': 'S16NFN',
            'sntxt': '[LOTCODE][DASH]PAC[SERIALNUMBER]',  # do not change
            'sndec': '[LOTCODE][SERIALNUMBER]',  # do not change
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
            'pcie': '1',  # x4
            'pmode': '0',
            'vcore': '550',
            'cba': '2',
            'cbb': '0',  # single
            'cbd': '1',
            'bmctemp': '99',
            'saktemp': '95',
            'boardtemp': '85',  # 85 for M2 and 80 for LP
            'pwren': '1',  # A only
            'saken': '1',  # A only
        },
    },
    'S2LP-D16 v1.5 for BMC 1.0.x':  {
        'lotcodes': {
            '52979': (14,28),
        },
        'parameters': {
            'name': 'S2LP',
            'var': 'D16BHN',
            'sntxt': '[LOTCODE][DASH]PAC[SERIALNUMBER]',  # do not change
            'sndec': '[LOTCODE][SERIALNUMBER]',  # do not change
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
            'pcie': '2',  # x8
            'pmode': '0',
            'vcore': '550',
            'cba': '2',
            'cbb': '2',  # dual
            'cbd': '1',
            'bmctemp': '99',
            'saktemp': '95',
            'boardtemp': '80',  # 85 for M2 and 80 for LP
            'pwren': '3',  # A and B
            'saken': '3',  # A and B
        },
    },
    'S2LP-S16 v1.5 for BMC 1.0.x':  {
        'lotcodes': {
            '52980': (1,5),
            # '52979': (15,15),  # dual -> single
            # 2025.02.19 converted back to dual for MR25 testing
            '52979+': (17,17),  # dual -> single
            '52979++': (23,23),  # dual -> single
        },
        'parameters': {
            'name': 'S2LP',
            'var': 'S16BHN',
            'sntxt': '[LOTCODE][DASH]PAC[SERIALNUMBER]',  # do not change
            'sndec': '[LOTCODE][SERIALNUMBER]',  # do not change
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
            'pcie': '2',  # x8
            'pmode': '0',
            'vcore': '550',
            'cba': '2',
            'cbb': '0',  # single
            'cbd': '1',
            'bmctemp': '99',
            'saktemp': '95',
            'boardtemp': '80',  # 85 for M2 and 80 for LP
            'pwren': '1',  # A only
            'saken': '1',  # A only
        },
    },
}  # end of foo

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
    for rawlotcode in cfg['lotcodes']:
        lotcode = rawlotcode.strip('+')  # plus sign may be used to add to lotcode
        checkdir(lotcode)  # create folder if missing
        checkdir(lotcode + '\\linux')
        start = ''
        end = ''
        for i in range(cfg['lotcodes'][rawlotcode][0], cfg['lotcodes'][rawlotcode][1] + 1):
            sn = '%03d' % i
            fname = 'cfg-edit-' + lotcode + '-PAC' + sn
            if len(start) == 0:
                start = '    ' + fname
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
        print(start + end)
# EOF

# @python.exe C:\EdgeCortix\HJS\statlog\statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+S2M2+S16NFN+10014[DASH]PAC001+10014001+1+5+0+2[DOT]01+20250117+20250123+1+0+2+800+1+0+550+2+0+1+99+95+85+1+1+C-fast
# @timeout 60
