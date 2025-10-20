# ae00 filters aetina logs

import os
import re

ver = '0.03'  # TBD

def debug(s):
    print(s.strip())

def validate(raw, filtered):
    status = True
    count = 'Count:'
    num = r'\s*?[0-9]+?.[0-9]+?'  # space(s) followed by ab.cd
    patterns = [  # python does a lot of -E stuff by default, and does NOT require escaping the dot char
        r'FTDI: [0-9]{8}',
        r'iSerial 3 [0-9]{8}',
        r'Board: EdgeCortix.+?[0-9]{5}-EC-[0-9]{3}, rev [0-9]+.[0-9]+',  # should allow double digit rev
        r'Secondary image, Revision .+?,',
        r'MAX,' + num + ',' + num + ',' + num + ',' + num + ',' + num,
        r'DETR\]',  # omit leading bracket for abbreviation
        r'ResNet50\]',  # omit leading bracket for abbreviation
        r'YoloV8\]',  # omit leading bracket for abbreviation
        r'Total latency:' + num + ' us',
        r't =' + num + ' s',  # elapsed time, may include non-homer entries
        # r'BIST 0: sakura',  # test case for wrapped saku\nra instance
        ]
    for pattern in patterns:
        a = re.findall(pattern, raw)
        b = re.findall(pattern, filtered)
        if a == b:
            print('Match: ' + str(a))
            count = count + ' ' + pattern[0] + str(len(a))
        else:
            print('Error: ' + str(a) + ' | ' + str(b))
            count = count + ' ' + pattern[0] + str(len(a)) + '|' + str(len(b))
            status = False
    print()
    print(count)
    return status
# End function

# read all files
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                rawlines = f.read()
                filteredlines = rawlines.replace('\n','')  # remove ALL newlines
                lines = rawlines.split('\n')  # split into list of lines
                if validate(rawlines, filteredlines):
                    print('Data is valid')
                else:
                    print('Data is corrupted')
                print()
                with open(filename + ' rawlines.txt', 'w', encoding='utf-8') as f:
                    f.write(rawlines)
                with open(filename + ' filteredlines.txt', 'w', encoding='utf-8') as f:
                    f.write(filteredlines + '\n')
                with open(filename + ' lines.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))

# EOF
