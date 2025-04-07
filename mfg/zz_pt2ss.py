# pt2ss generates a dictionary, webpage (eventually), and spreadsheet(s) based on all of the prodtest files in the repo
import os

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'
DO_PAUSE = True  # for timer at end

# set path based on OS
if WINDOWS:
    ptpath = 'C:\\EdgeCortix\\prodtest\\'
elif LINUX:
    ptpath = '/home/ec/prodtest/'
else:
    print('Unknown OS')
    ptpath = '.'

# containers
foo = {}  # good info
bar = {}  # todo list
sns = []  # list of serial numbers to sort and iterate

# FUNCTIONS

def GetKey(a, b, c, d, e):
    return a + '.' + b + ' (' + c + '-' + d + ' rev' + e + ')'
# End

def ModKey(key, node):
    return key[0:13] + node + key[14:]
# End

def summarize(lines, dirname, filename):
    global foo
    global bar
    global sns
    prod = 'error'  # Board parameter
    var = 'error'  # Board parameter
    ser = 'error'  # Board parameter
    node = 'error'  # Board parameter
    rev = 'error'  # Board parameter
    key = GetKey(ser, node, prod, var, rev)  # default key, overwritten by fn call later
    tsak = 'error'  # sakura temperature
    pri = 'Unk'  # BMC Software parameter, Pri or Sec
    bmc = 'h.j.s'  # BMC Software parameter
    for rawline in lines:
        line = rawline.strip()
        if len(line) == 0:  # blank, discard
            pass
        elif line.startswith("\0"):  # starts with null char, discard
            print('NULL in ' + filename)
        elif line.startswith('HJS WAS HERE'):  # line that was manually edited by HJS, discard
            with open ('zzhjs.tsv', 'a') as f:
                f.write('............' + line[12:] + ' in ' + filename + '\n')
        elif line.startswith('[['):  # debug section header, discard completely
            pass
        elif 'Failed to open' in line:  # serial port not connected during prodtest, discard
            pass
        # start of tsv files
        elif 'powerDownS2LP fault code' in line or 'powerDownS2M2: fault' in line:  # store in tsv, text format may change!
            with open ('zzfault.tsv', 'a') as f:  # append log
                f.write(line + '\n')
        elif line.startswith('cfg.edit'):  # cfg edit, store in tsv
            with open ('zzcfg.tsv', 'a') as f:  # append log
                f.write('  ' + key + '\n')
                f.write('    ' + line + '\n')
        elif line.startswith('Subsystem:') or line.startswith('Region ') or line.startswith('LnkSta:') or 'Co-processor: Device' in line:  # 1fdc, store in tsv
            with open ('zz1fdc.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('[') and '->' in line:  # statlog type 1, first line in prodtest log
            with open ('zzstatlog.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif '[\'stats\']' in line:  # statlog type 2, called stats
            with open ('zzstatlog.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('idVendor') or line.startswith('idProduct') or line.startswith('iManufacturer') or line.startswith('iProduct') or line.startswith('iSerial'):  # five FTDI prefixes
            with open ('zzftdi.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'srread a 0xC008C' in line:  # PCIe status
            with open ('zzpciestatus.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('AEN_PG') or line.startswith('BEN_PG') or line.startswith('M2EN_PG'):  # BMC pins
            with open ('zzbmcpins.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('LAST,'):
            with open ('zzlast.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('MEAN,'):
            with open ('zzmean.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'BIST: sakura A' in line or 'BIST: sakura B' in line or 'BIST: Sakura A' in line or 'BIST: Sakura B' in line:  # BIST
            with open ('zzbist.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('Trial') or line.startswith('ALL DMA') or line.startswith('Testing Device') or line.startswith('PASSED - device') or line.startswith('FAILED - device') or line.startswith('ERROR: One or more DMA tests failed'):  # dma_test
            with open ('zzdma_test.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif '[QUOTE][STAR]' in line or 'Name Pin Pfs Mode Val Drive' in line or '-quotestar-' in line or line.startswith('bmc bin ->') or line.startswith('./bmc [bin] ->'):  # BMC spam
            with open ('zzbmcspam.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'sakuraDriver wait' in line or 'sakuraDriver read' in line or 'sakuraDriver write' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'maxInit U26' in line or 'maxInit U30' in line or 'maxInit U46' in line or 'maxInit U50' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'powerUpS2LP: error' in line or 'powerUpS2M2: error' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'srread error -1' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'ihex parse error' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'eeprom init failed' in line:  # ignore these errors, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif 'sakuraStart: status 0, PASS' in line:  # legacy, send to bugs
            with open ('zzbugs.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('0:') or line.startswith('1:') or line.startswith('2:') or line.startswith('3:') or line.startswith('4:'):  # xlog?
            with open ('zzxlog.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        elif line.startswith('5:') or line.startswith('6:') or line.startswith('7:') or line.startswith('8:') or line.startswith('9:'):  # xlog?
            with open ('zzxlog.tsv', 'a') as f:
                f.write(line + '\n')  # append log
        # end of tsv files, start of dict
        elif line.startswith('Board: '):  # generates key
            x = line.split(',')
            if len(x) == 4:
                prod = x[0][-4:]  # last four are product name
                var = x[1].strip()[8:].ljust(6)  # index 1 is variant, remove 'variant ' prefix, force len=6
                ser = x[2].strip()[4:]  # index 2 is serial number, remove 'ser ' prefix
                node = 'A'
                rev = x[3].strip()[4:].ljust(3)  # index 3 is rev, remove 'rev ' prefix, force len=3
            else:
                print('In ' + filename)
                print('Wrong token count: ' + line)
                prod = 'ZZZZ'
                var = 'ABCDEF'
                ser = 'XXXXX-sepYYY'  # SNSEP resolved
                node = '?'
                rev = 'GHI'
            key = GetKey(ser, node, prod, var, rev)
            # print(ser + ' ' + prod + ' ' + var + ' ' + rev)
        elif line.startswith('BMC Software:'):  # BMC info, expands key
            pri = line[14:17]
            x = line.split(',')
            bmc = x[1].strip()[9:]  # middle token, stripped, starting after 'Revision '
            if key.startswith('error'):
                print(pri + ' | ' + bmc)  # bad key, print line
            else:
                key = key + ' [' + pri + ' ' + bmc + ']'
        elif line.startswith('VAL,'):  # node info, expands key
            if 'T_SAKA' in line:  # LP, A
                node = 'A'
            elif 'T_SAKB' in line:  # LP, B
                node = 'B'
            elif 'T_SAK' in line:  # M2, A
                node = 'A'
            key = ModKey(key, node)  # modify key
        elif line.startswith('MAX,'):  # dict info
            x = line.split(',')
            if len(x) == 6:
                tsak = x[4].strip()  # index 4 is sakura temperature on M.2
            elif len(x) == 17:
                tsak = x[11].strip()  # index 11 is sakura temperature on LP
            elif len(x) == 15:
                tsak = x[11].strip()  # index 11 is sakura temperature on LP with power failure
            else:
                print('In ' + filename)
                print('Wrong token count: ' + line)
                tsak = '-1'
            try:
                foo[key]['tsak'].append(tsak)  # try to append to existing list
            except:
                foo[key] = {}  # new blank dict
                foo[key]['tsak'] = [tsak,]  # make new list with current entry
                sns.append(key)  # list to be sorted later
        # end of dict
        elif line[0].isprintable:  # check if start char is printable, report bad line
            print('In: ' + dirname + ' in ' + filename)
            print('badline: [' + line + ']')
            # print('-'.join([str(ord(character)) for character in line]) + '\n')
        else:  # unprintable chars are discarded entirely, report bad line
            print('In: ' + dirname + ' in ' + filename)
            print('-'.join([str(ord(character)) for character in line]) + '\n')
# End

# END FUNCTIONS

# prep dump files
with open ('zzfault.tsv', 'w') as f:
    f.write('fault [Fault Codes]:\n')
with open ('zzcfg.tsv', 'w') as f:
    f.write('cfg-edit:\n')
with open ('zz1fdc.tsv', 'w') as f:
    f.write('1fdc:\n')
with open ('zzstatlog.tsv', 'w') as f:
    f.write('statlog:\n')
with open ('zzftdi.tsv', 'w') as f:
    f.write('ftdi:\n')
with open ('zzpciestatus.tsv', 'w') as f:
    f.write('PCIe status:\n')
with open ('zzbmcpins.tsv', 'w') as f:
    f.write('BMC pins:\n')
with open ('zzlast.tsv', 'w') as f:
    f.write('LAST:\n')
with open ('zzmean.tsv', 'w') as f:
    f.write('MEAN:\n')
with open ('zzbist.tsv', 'w') as f:
    f.write('BIST:\n')
with open ('zzdma_test.tsv', 'w') as f:
    f.write('DMA test:\n')
with open ('zzbmcspam.tsv', 'w') as f:
    f.write('BMC spam:\n')
with open ('zzbugs.tsv', 'w') as f:
    f.write('Bugs:\n')
with open ('zzxlog.tsv', 'w') as f:
    f.write('XLOGs:\n')
with open ('zzhjs.tsv', 'w') as f:
    f.write('HJS WAS HERE:\n')

# read all files
filecount = 0
for dirname, dirnames, filenames in os.walk(ptpath):  # get info from prodtest folder
    for filename in filenames:
        if filename.endswith('.txt') and '-0x' in filename and filename.startswith('10015'):  # check extension, SN/TS separator, lotcode
            filecount = filecount + 1
            if filecount % 10 == 0:  # add dot every 10
                print('.', end='')
            if filecount % 100 == 0:  # add newline every 100
                print()
            with open(os.path.join(dirname,filename), 'r') as f:
                summarize(f.readlines(), dirname, filename)
sorted_sns = sorted(sns)
with open ('zzpt.tsv', 'w') as f:
    last_ser = ''
    for ser in sorted_sns:
        if ser[0:5] != last_ser[0:5]:  # compare lot codes
            f.write('\n')  # blank line if new lot code
        sorted_tsak = sorted(foo[ser]['tsak'], reverse=True)
        f.write(ser + '\t' + '\t'.join(sorted_tsak) + '\n')
        last_ser = ser  # save for next loop

print('\nFile count: ' + str(filecount))  # print file count
if WINDOWS and DO_PAUSE:
    os.system('timeout /t 60')  # windows only, keep window open, keystroke ends it instantly        

# EOF

# Notes

"""
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A,  V_P3V3,   V_P12V
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A
VAL,  V_P3V3,    I_3V3,   TEMP,      T_SAK,    P_P3V3
"""
