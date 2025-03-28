import os
import ast
import yaml  # pip install pyyaml

# list of short mfg names
replaceMFG = {
    'Analog Devices Inc./Maxim Integrated': 'Analog Devices/Maxim',
    'FTDI, Future Technology Devices International Ltd': 'FTDI',
    'Renesas Electronics Corporation': 'Renesas',
}


configs = {}
note = ''
def ReadYAML(filename):
    global configs
    global note
    try:
        with open(filename, 'r') as f:
            configs = yaml.safe_load(f)
    except:
        pass  # configs will be blank
    if 'Note' in configs:
        note = configs['Note']
        del configs['Note']  # remove so it doesn't appear as a project
        print('\nNote: ' + note)
    for project in configs:
        if '_ALL_' not in configs[project]:
            configs[project]['_ALL_'] = {}  # blank dict
        for config in configs[project]:
            if 'add' not in configs[project][config]:
                configs[project][config]['add'] = {}  # blank dict
            if 'dni' not in configs[project][config]:
                configs[project][config]['dni'] = []  # blank list
            if 'sub' not in configs[project][config]:
                configs[project][config]['sub'] = {}  # blank dict
    # print(configs)
# End


def GetFiles():
    bom = ''
    net = ''
    for filename in os.listdir():  # only look in current folder
        n = filename.lower()  # only used for checking extension
        if n.endswith('.dict'):
            # print('Found ' + filename)  # debug
            if '.csv converted to' in n:
                bom = filename
            elif '.net converted to' in n:
                net = filename
    if bom == '' or net == '':
        print('This script requires two files: csv and net, converted to dict.')
        return ['error',]  # list length = 1 implies error
    else:
        return [bom,net]  # list of valid files
# End


def GetDict(filename):
    with open(filename, 'r') as f:
        file = f.read()
    dict = ast.literal_eval(file)
    return dict
# End


def VerifyAttribute(dict, k, s0, s1):
    for a in dict['comps'][k]['attributes']:
        if a[0] == s0 and a[1] == s1:
            return True
    return False
# End


def GetKeys(bom, net):
    bomkeys = []
    netkeys = []
    for k in bom:
        bomkeys.append(k)
    for k in net['comps']:
        netkeys.append(k)
    # print(' '.join(bomkeys))  # debug
    # print(' '.join(netkeys))  # debug
    missing = ''
    for k in bomkeys:
        if k not in netkeys:
            missing = missing + ' ' + k
    if len(missing) > 0:
        print('  Missing from Netlist: ' + missing)
    missing = ''
    bom_ignore = ''
    bom_ignore_tp = ''
    bom_ignore_tp_count = 0
    for k in netkeys:
        if k not in bomkeys:
            if VerifyAttribute(net, k, 'BOM_IGNORE', 'true'):
                if k.startswith('TP'):  # test points are often numerous
                    bom_ignore_tp_count = bom_ignore_tp_count + 1
                    bom_ignore_tp = ' TPxx (' + str(bom_ignore_tp_count) + ')'
                else:  # not a test point
                    bom_ignore = bom_ignore + ' ' + k
            else:
                missing = missing + ' ' + k
    if len(bom_ignore) > 0 or len(bom_ignore_tp) > 0:
        print('  Ignored:' + bom_ignore + bom_ignore_tp)
    if len(missing) > 0:
        print('  Missing from BOM:' + missing)
    return bomkeys  # should be the same as netkeys not counting ignores
# End


def GetColumns(bom, net, keys):
    bom_columns = ['ECPN', 'MFG', 'MPN', 'Description']
    net_columns = ['PART_NUMBER', 'Manufacturer', 'Manufacturer PN', 'Description']
    bom_info = {}
    net_info = {}
    for refdes in keys:
        bom_row = []
        try:  # in case keys didn't match, this could fail
            for column in bom_columns:
                bom_row.append(bom[refdes][column])
            bom_info[refdes] = bom_row
        except:
            pass
        net_row = []
        try:  # in case keys didn't match, this could fail
            for column in net_columns:
                net_row.append(net['comps'][refdes][column])
            if 'BuildOptions' in net['comps'][refdes]:  # may or may not be present
                net_row.append(net['comps'][refdes]['BuildOptions'])
            net_info[refdes] = net_row
        except:
            pass
    combined = {}
    for refdes in keys:  # each line should contain four list elements
        bom_line = 'ERROR'
        net_line = 'ERROR'
        try:
            bom_line = bom_info[refdes]
            net_line = net_info[refdes][0:4]  # remove possible BuildOptions entry
            if len(refdes) > 1:  # should be at least 2
                longrefdes = refdes[0] + refdes[1:].rjust(9, '0')  # assumes only single char refdes
            else:
                longrefdes = refdes
            if bom_line != net_line:
                print('  Mismatch in: ' + refdes + '\n    ' + str(bom_line) + '\n    ' + str(net_line))
            combined[longrefdes] = [refdes,] + net_info[refdes]
        except:
            print('  Error in: ' + refdes + '\n    ' + str(bom_line) + '\n    ' + str(net_line))
    return combined
# End


def WriteCondensed(filename, condensed):
    condensed_file = filename + '-condensed.tab'
    dni_input = filename + '-DNI.tab'
    refdescount = 0
    with open(condensed_file, 'w') as f:
        f.write('\t'.join(['ECPN','QTY','RefDes','MFG','MPN','Description']) + '\n')
        if note != '':
            f.write('\t\t' + note + '\n')  # add note if it exists
        for ecpn in condensed:
            mfg = condensed[ecpn][0]
            refdeslist = condensed[ecpn][3:]
            qty = len(refdeslist)  # count refdes
            refdescount = refdescount + qty
            refdes = ', '.join(refdeslist)  # join refdes with comma and space
            out = [ecpn, str(qty), refdes, mfg] + condensed[ecpn][1:3]  # create new list
            f.write('\t'.join(out) + '\n')  # write tab data and newline
        with open(dni_input, 'r') as fin:
            dni_lines = fin.read()
        f.write(dni_lines)  # add DNI lines to condensed
    print('Wrote ' + str(refdescount) + ' RefDes to condensed BOM')
# End


def PrintSubSummary(old, new, last):  # each list is ecpn/mfg/mpn/desc
    old_mmd = old[1:4]
    new_mmd = new[1:4]
    strlen = [len(x) for x in old_mmd] + [len(y) for y in new_mmd]
    maxlen = max(strlen)
    padded_old = [old[0] + ' ='] + [x.ljust(maxlen+2) for x in old_mmd]
    padded_new = [new[0] + ' ='] + [x.ljust(maxlen+2) for x in new_mmd]
    summary = '  Sub: ' + ' '.join(padded_old) + '\n' + '       ' + ' '.join(padded_new)
    if summary != last:  # only print if different 
        print(summary)
    return summary
# End


def WriteFile(project, config, dni_list, sub_list, add_list, all, sorted_refdes):
    condensed = {}
    filename = project + '-' + config
    with open(filename + '.tab', 'w') as f:
        count = 0
        dnicount = 0
        with open(filename + '-DNI.tab', 'w') as fdni:
            print('\n' + project + '-' + config)
            print('DNI = ' + '|'.join(dni_list))
            for add_list_key in add_list:
                print('ADD = ' + add_list_key + ' -> ' + '|'.join(add_list[add_list_key]))
                condensed[add_list_key] = add_list[add_list_key]
            for sub_list_key in sub_list:
                print('SUB = ' + sub_list_key + ' -> ' + '|'.join(sub_list[sub_list_key]))
            last_summary = ''  # records last summary to avoid duplicates
            option_count = {}  # will contain counts of option strings
            for k in sorted_refdes:
                add_to_condensed = False
                this_line = all[k].copy()  # need to modify temporarily
                ecpn = this_line[1]
                if this_line[2] in replaceMFG:  # check if MFG is a long name
                    this_line[2] = replaceMFG[this_line[2]]  # use replacement string
                if ecpn in sub_list:
                    last_summary = PrintSubSummary(this_line[1:5], sub_list[ecpn], last_summary)
                    this_line[1] = sub_list[ecpn][0]  # there must be a better way
                    this_line[2] = sub_list[ecpn][1]
                    this_line[3] = sub_list[ecpn][2]
                    this_line[4] = sub_list[ecpn][3]
                new_bom_line = '\t'.join(this_line)
                if len(this_line) == 6:  # has BuildOptions
                    build_option_value = this_line[5]
                    build_options = build_option_value.split('(', 1)[0].strip()  # remove any comment in parentheses, such as (w/ subs)
                    if build_options in dni_list:
                        reorder = this_line[1] + '\t0\t' + this_line[0] + ' (' + this_line[5] + ')\t' +  '\t'.join(this_line[2:5])
                        fdni.write(reorder + '\n')
                        dnicount = dnicount + 1
                    else:
                        f.write(new_bom_line + '\n')
                        add_to_condensed = True
                    try:
                        option_count[build_options] = option_count[build_options] + 1
                    except:
                        option_count[build_options] = 1
                else:  # no build options
                    f.write(new_bom_line + '\t-\n')  # add dash for blank column
                    add_to_condensed = True
                if add_to_condensed:
                    count = count + 1
                    if ecpn not in condensed:
                        condensed[ecpn] = this_line[2:5]  # columnns 2/3/4 are MFG, MPN, DESC
                    condensed[ecpn].append(this_line[0])  # append refdes to existing ecpn's list
                    if this_line[2] != condensed[ecpn][0] or this_line[3] != condensed[ecpn][1] or this_line[4] != condensed[ecpn][2]:
                        print('Mismatch in ' + this_line[0] + ':')
                        print('  ' + '|'.join(this_line[2:5]))  # MFG, MPN, DESC
                        print('  ' + '|'.join(condensed[ecpn][0:3]))  # MFG, MPN, DESC
            print('Found option strings:')
            for c in option_count:
                print('  ' + c + ': ' + str(option_count[c]))
            print('Count ' + str(count) + ' (DNI Count ' + str(dnicount) + ', Total ' + str(count+dnicount) + ')')
    # print(condensed)  # debug
    WriteCondensed(filename, condensed)
# End


def WriteFiles(files, all):
    refdes = []
    for k in all:
        refdes.append(k)  # create list of sortable refdes
    sorted_refdes = sorted(refdes)  # sort them
    filename = 'all.tab'
    with open(filename, 'w') as f:
        f.write('\t'.join(['RefDes', 'ECPN', 'MFG', 'MPN', 'Description', 'BuildOptions']) + '\n')  # header
        for k in sorted_refdes:
            if len(all[k]) == 5:  # no build options, RefDes thru Desc
                f.write('\t'.join(all[k]) + '\t-\n')  # add dash for BuildOptions
            else:
                f.write('\t'.join(all[k]) + '\n')  # should be all six columns
    print('\nWrote ' + filename)
    print('Count: ' + str(len(sorted_refdes)))
    for project in configs:
        if project.lower() in files[0].lower():  # only analyze if the project is in the bom filename
            for config in configs[project]:
                if config != '_ALL_':  # not meant to be written
                    WriteFile(
                        project,
                        config,
                        configs[project]['_ALL_']['dni'] + configs[project][config]['dni'],  # merge lists
                        configs[project][config]['sub'],
                        configs[project]['_ALL_']['add'] | configs[project][config]['add'],  # merge dicts
                        all,
                        sorted_refdes
                    )
# End


# start of script
print()  # blank line to separate from prompt
files = GetFiles()
if len(files) == 2:
    print('Analyzing:\n  ' + '\n  '.join(files))
    bom = GetDict(files[0])
    net = GetDict(files[1])
    keys = GetKeys(bom, net)
    # print(keys)  # debug
    print('Count: ' + str(len(keys)))
    all = GetColumns(bom, net, keys)
    ReadYAML('BOM.yaml')
    WriteFiles(files, all)

if note != '':
    configs['Note'] = note
with open('BOM.yaml', 'w') as f:
    yaml.dump(configs, f)
print()
os.system("PAUSE")
# EOF
