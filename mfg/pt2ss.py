# pt2ss generates a dictionary, webpage, and spreadsheet from prodtest files
import os
import pprint

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

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

def summarize(lines, dirname, filename):
    global foo
    global bar
    global sns
    ser = 'error'
    tsak = 'error'
    for rawline in lines:
        line = rawline.strip()
        if len(line) == 0:  # blank
            pass
        elif line.startswith("\0"):  # starts with null char
            pass
        elif line.startswith('WTF'):  # line that was manually edited by HJS
            pass
        elif 'Failed to open' in line:  # serial port not connected during prodtest
            pass
        elif line.startswith('Board: '):
            x = line.split(',')
            if len(x) == 4:
                ser = x[2].strip()  # index 2 is serial number
            else:
                print('In ' + filename)
                print('Wrong token count: ' + line)
                ser = 'ser XXXXX-PACYYY'
        elif line.startswith('BMC Software:'):  # BMC?
            pass
        elif line.startswith('[') and '->' in line:  # statlog?
            pass
        elif '[\'stats\']' in line:  # statlog called stats
            pass
        elif line.startswith('Subsystem:'):  # 1fdc?
            pass
        elif line.startswith('Region '):  # 1fdc?
            pass
        elif line.startswith('LnkSta:'):  # 1fdc?
            pass
        elif 'Co-processor: Device' in line:  # 1fdc?
            pass
        elif line.startswith('Trial'):  # dma_test?
            pass
        elif line.startswith('ALL DMA'):  # dma_test?
            pass
        elif line.startswith('Testing Device'):  # dma_test?
            pass
        elif line.startswith('PASSED - device'):  # dma_test?
            pass
        elif line.startswith('FAILED - device'):  # dma_test?
            pass
        elif line.startswith('ERROR: One or more DMA tests failed'):  # dma_test?
            pass
        elif 'srread a 0xC008C' in line:  # PCIe?
            pass
        elif line.startswith('idVendor'):  # FTDI
            pass
        elif line.startswith('idProduct'):  # FTDI
            pass
        elif line.startswith('iManufacturer'):  # FTDI
            pass
        elif line.startswith('iProduct'):  # FTDI
            pass
        elif line.startswith('iSerial'):  # FTDI
            pass
        elif line.startswith('AEN_PG') or line.startswith('BEN_PG') or line.startswith('M2EN_PG'):  # BMC pins?
            pass
        elif '[QUOTE][STAR]' in line or 'Name Pin Pfs Mode Val Drive' in line or '-quotestar-' in line:  # BMC spam
            pass
        elif line.startswith('0:'):  # xlog?
            pass
        elif line.startswith('VAL,'):
            pass
        elif line.startswith('LAST,'):
            pass
        elif line.startswith('MEAN,'):
            pass
        elif line.startswith('MAX,'):
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
                foo[ser[4:]].append(tsak)  # try to append to existing list
            except:
                foo[ser[4:]] = [tsak]  # make new list with current entry
                sns.append(ser[4:])  # list to be sorted later
        elif 'BIST: sakura A' in line:  # BIST?
            pass
        elif 'BIST: sakura B' in line:  # BIST?
            pass
        elif 'BIST: Sakura A' in line:  # BIST? cap S
            pass
        elif 'BIST: Sakura B' in line:  # BIST? cap S
            pass
        elif 'sakuraDriver wait' in line or 'sakuraDriver read' in line:  # ignore these errors
            pass
        elif 'maxInit U26' in line or 'maxInit U30' in line or 'maxInit U46' in line or 'maxInit U50' in line:  # ignore these errors
            pass
        elif 'srread error -1' in line:  # ignore these errors
            pass
        elif 'eeprom init failed' in line:  # ignore these errors
            pass
        elif 'sakuraStart: status 0, PASS' in line:  # legacy
            pass
        elif line[0].isprintable:  # check if start char is printable
            print('In: ' + dirname + ' in ' + filename)
            print('badline: [' + line + ']')
            # print('-'.join([str(ord(character)) for character in line]) + '\n')
        else:  # unprintable chars are discarded entirely
            print('In: ' + dirname + ' in ' + filename)
            print('-'.join([str(ord(character)) for character in line]) + '\n')
# End

# END FUNCTIONS

# read all files
for dirname, dirnames, filenames in os.walk(ptpath):  # get info from prodtest folder
    for filename in filenames:
        if filename.endswith('.txt') and '-0x' in filename:  # check extension and SN/TS separator
            with open(os.path.join(dirname,filename), 'r') as f:
                summarize(f.readlines(), dirname, filename)
# pprint.pprint(foo)
sorted_sns = sorted(sns)
with open ('pt.tsv', 'w') as f:
    last_ser = ''
    for ser in sorted_sns:
        if ser[0:5] != last_ser[0:5]:  # compare lot codes
            f.write('\n')  # blank line if new lot code
        sorted_tsak = sorted(foo[ser], reverse=True)
        f.write(ser + '\t' + '\t'.join(sorted_tsak) + '\n')
        last_ser = ser  # save for next loop
        
# EOF

# Notes

"""
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A,  V_P3V3,   V_P12V
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A
VAL,  V_P3V3,    I_3V3,   TEMP,      T_SAK,    P_P3V3
"""
