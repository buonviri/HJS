# ae00 filters aetina logs

import os

ver = '0.00'  # TBD

def debug(s):
    print(s.strip())

def fixnewlines(s):
    badwords = [
        ('saku\nra', 'sakura'),
        ]
    fixed = s  # make a copy
    for word in badwords:
        fixed = fixed.replace(word[0], word[1])
    return fixed

def filter(s):
    result = []
    for line in s:
        if line.startswith('______') or line.startswith('|  ____|') or line.startswith('| |') or line.startswith('|  __|') or line.startswith('|_____') or line.startswith('__/ |') or '|___/' in line:
            debug(line)  # splash screen
        else:
            result.append(line)
    return '\n'.join(result)

# read all files
for dirname, dirnames, filenames in os.walk('.'):  # get info from current folder
    for filename in filenames:
        if filename.endswith('.log'):  # check extension
            with open(os.path.join(dirname,filename), 'r', encoding='utf-8') as f:
                result = fixnewlines(f.read())
                result = filter(result.split('\n'))
                with open(filename + ' new.txt', 'w', encoding='utf-8') as f:
                    f.write(result + '\n')

# EOF
