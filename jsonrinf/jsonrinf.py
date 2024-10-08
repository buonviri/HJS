import os
import re
import pprint

# generates JSON file and clipboard:
#   header included
#   components section
#   nets section

if os.name == 'nt':  # clipboard generally only works in windows
    try:
        import pyperclip
        clipboard = True
    except:
        print('\nRequires pyperclip. Use: pip install pyperclip')
        clipboard = False

double_quotes = '"“”'  # this string includes the standard one, chr(34), as well as the left and right versions


def GetTokens(x):  # standard function for splitting strings containing quoted strings
    return [p for p in
        re.split("( |\\\".*?\\\"|'.*?')", x.strip()) if p.strip()]
# end of GetTokens()


def WriteSortedNetlist(lines):
    found_comp = False
    pre = []
    comp = []
    attr = []
    post = []
    for rawline in lines:
        line = rawline.rstrip()  # strip newline, keep indentation
        if line.startswith('.ADD_COM'):
            found_comp = True  # determines pre vs post for fluff
            comp.append(line)
        elif line.startswith('.ATT_COM'):
            attr.append(line)
        elif found_comp:
            post.append(line)
        else:
            pre.append(line)
    with open('sorted.txt', 'w') as f:
        f.write('\n'.join(pre) + '\n')
        f.write('\n'.join(sorted(comp)) + '\n')
        f.write('\n'.join(sorted(attr)) + '\n')
        f.write('\n'.join(post) + '\n')
# End


def convert(lines):
    WriteSortedNetlist(lines)  # for easier comparison between git revs
    info = {'comps': {}, 'nets': {}}  # blank dict for storing all netlist info
    lastline = ''  # contains keyword of last line
    # list of words that aren't useful:
    badwords = {'.HEA': 'header',
                '.TIM': 'timestamp',
                '.APP': 'application',
                '.UNI': 'units',
                '.TYP': 'type',
                '.JOB': 'job',
                '.END': 'end',
                }
    # list of words that contain info:
    keywords = {'.ADD': 'add...',  # should be followed by _COM or _TER
                '.ATT': 'attribute',  # usually followed by _COM, can also be _TRE in nets
                '.TER': 'pin',
                }
    device = 'UUU999'  # fake device
    pin = '123456'  # fake pin
    netname = 'HOMER SEZ NO NET (ERROR)'  # (hopefully) invalid netname
    addcomcount = 0
    bomignorecount = 0
    att_tre_count = 0
    for rawline in lines:
        line = rawline.strip().replace('\t',' ')  # strip newline and spaces, replace tab with space
        if len(line) == 0:
            pass  # do nothing with blanks lines
        elif line.startswith('#'):
            pass  # this line is a comment, same as in python
        elif line[0:4] in badwords:  # matches known bad word
            lastline = line[0:4]  # save for next loop
            try:
                info[line[0:4]].append(line[4:].strip().strip(double_quotes))  # try to append remainder of line to list
            except:
                info[line[0:4]] = [line[4:].strip().strip(double_quotes),]  # make new list
        elif line[0:4] in keywords:  # matches known keyword
            lastline = line[0:4]  # save for next loop
            if line.startswith('.ADD_COM'):
                addcomcount = addcomcount + 1
                words = GetTokens(line[8:].strip())
                device = words[0]  # refdes
                devinfo = [x.strip(double_quotes) for x in words[1:]]  # list of remaining tokens with quotes removed
                info['comps'][device] = {'part': [], 'attributes': []}  # new dictionary for this refdes
                info['comps'][device]['part'].append(devinfo)  # add info to this refdes
            elif line.startswith('.ATT_COM'):
                if 'BOM_IGNORE' in line:
                    if 'true' in line.lower():
                        bomignorecount = bomignorecount + 1
                    else:
                        print('  BOM_IGNORE line found but value is not true: ' + line)
                words = GetTokens(line[8:].strip())
                device = words[0]  # refdes
                attrinfo = [x.strip(double_quotes) for x in words[1:]]  # list of remaining tokens with quotes removed
                info['comps'][device]['attributes'].append(attrinfo)  # add info to this refdes, assumes ADD_COM already happened!
                if len(attrinfo) == 2:  # this should always be the case
                    info['comps'][device][attrinfo[0]] = attrinfo[1]
                else:
                    print('Questionable attribute list: ' + str(attrinfo))
            elif line.startswith('.ADD_TER'):
                words = GetTokens(line[8:].strip())
                device = words[0]  # refdes
                pin = words[1]
                netname = words[2].strip(double_quotes)
                # note that words[3] *might* exist, as a comment
                info['nets'][netname] = [(device,pin),]  # create new list with one tuple
                # print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
            elif line.startswith('.TER'):
                words = GetTokens(line[4:].strip())
                device = words[0]  # refdes
                pin = words[1]
                # net name is inherited from earlier line
                # note that words[2] *might* exist, as a comment
                info['nets'][netname].append((device,pin))  # append list with new tuple
                # print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
            elif line.startswith('.ATT_TRE'):
                att_tre_count = att_tre_count + 1
            else:
                print('  No match: ' + line)
        elif lastline == '.TER':  # special case, additional .TER lines don't need keyword
            words = GetTokens(line.strip())
            if len(words) > 1:  # should contain two or more words
                device = words[0]  # refdes
                pin = words[1]
                # net name is inherited from earlier line
                # note that words[2] *might* exist, as a comment
                info['nets'][netname].append((device,pin))  # append list with new tuple
                # print(device.ljust(10) + ' ' + pin.ljust(5) + ' ' + netname)
            else:
                print('Bad line: ' + line)
        else:
            print('Bad line: ' + line)
    print('  ADD_TRE discarded: ' + str(att_tre_count))
    print('  ADD_COM count: ' + str(addcomcount))
    print('  BOM_IGNORE count: ' + str(bomignorecount))
    print('  BOM should have ' + str(addcomcount-bomignorecount) + ' entries')
    return info
# end of convert()


# start of script
print()  # blank line to separate from prompt
for filename in os.listdir():  # only look in current folder
    n = filename.lower()  # only used for checking extension
    if n.endswith('.frp') or n.endswith('.net'):
        name = filename + ' converted to.dict'
        print('Writing: ' + name)
        with open(filename, 'r') as f:
            info = convert(f.readlines())  # read entire file and pass as a list
        with open(name, 'w') as f:
            formatted = pprint.pformat(info, indent=2, width=200)
            f.write(formatted + '\n')  # write using pformat
        print('  Done\n')
# end of main loop

print('All double quotes have been removed:')
for c in double_quotes:
    print('  ' + c + ' = chr(' + str(ord(c)) + ')')

if clipboard:
    pyperclip.copy(formatted)
    print('\nInfo written to clipboard')

print()
os.system("PAUSE")
# EOF
