import os

mypath = 'C:\\EdgeCortix\\S2-BMC\\'

filecount = 0

print('Searching: ' + mypath + '\n')
for dirname, dirnames, filenames in os.walk(mypath):
    for filename in filenames:
        # print(filename)
        if filename.endswith('.ld') or filename.endswith('Shims.h'):  # any linker file, or header file containing version
            filecount = filecount + 1
            fullpath = os.path.join(dirname, filename)
            with open(fullpath) as f:
                lines = f.readlines()
                header = '  ' + fullpath
                goodlines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('INCLUDE memory_regions') or stripped.startswith('FLASH_START = 0x'):
                        goodlines.append('    ' + line.strip())  # add to goodlines
                    if stripped.startswith('#define BMC_REVISION'):
                        goodlines.append('    ' + line.strip())  # add to goodlines
                if len(goodlines) > 0:  # only print if at least one line was found
                    print(header)
                    print('\n'.join(goodlines) + '\n')

print('Files analyzed: ' + str(filecount))

os.system("PAUSE")

# EOF
