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

def summarize(lines, filename):
    global foo
    global bar
    global sns
    ser = 'error'
    tsak = 'error'
    for rawline in lines:
        line = rawline.strip()
        if line.startswith('Board: '):
            x = line.split(',')
            if len(x) == 4:
                ser = x[2].strip()  # index 2 is serial number
            else:
                print('In ' + filename)
                print('Wrong token count: ' + line)
                ser = 'ser XXXXX-PACYYY'
        if line.startswith('MAX,'):
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
# End

# END FUNCTIONS

# read all files
for dirname, dirnames, filenames in os.walk(ptpath):  # get info from prodtest folder
    for filename in filenames:
        if filename.endswith('.txt') and '-0x' in filename:  # check extension and SN/TS separator
            with open(os.path.join(dirname,filename), 'r') as f:
                summarize(f.readlines(), filename)
# pprint.pprint(foo)
sorted_sns = sorted(sns)
with open ('pt.tsv', 'w') as f:
    for ser in sorted_sns:
        sorted_tsak = sorted(foo[ser], reverse=True)
        f.write(ser + '\t' + '\t'.join(sorted_tsak) + '\n')
        
# EOF

# Notes

"""
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A,  V_P3V3,   V_P12V
VAL,   I_12V_BP, I_3V3_BP,  I_CB_A0, I_CB_A12, I_0V75_A,  I_0V8_A,  I_1V8_A,  I_1V1_A,  I_0V6_A,   T_WEST,   T_SAKA,  P_TOTAL,  P_DDR_A,  P_SAK_A
VAL,  V_P3V3,    I_3V3,   TEMP,      T_SAK,    P_P3V3
"""
