# sends commands to S1/S2

import sys
try:
    import serial  # requires pip install pyserial
    import serial.tools.list_ports
except:
    print('Serial Number  = [Failed to import pyserial]')  # emulate actual response
    sys.exit(0)
import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir

import pprint  # temp

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

# set columns and rows in Windows
cols = 100
rows = 40

# set delay between log entries (in seconds)
logdelay = 3

# initialize log timer to 1970
lastlog = 0

# determines if the script pauses at the end, etc
do_pause = True
do_slow = False
verbose = True
null = False
void_msg = ''  # if void flag is used, this stores the one message that gets printed
# add new entries to flags() function as well

# set product name, default is S1LP for historical purposes
my_product = 'S1LP'


def stat(dev):
    dev.write(b'stat\n')
    val = dev.read(99999)
    return val.decode('utf-8').strip()
# End


def other(dev, cmd):
    dev.write(bytes(cmd + '\n', 'utf-8'))
    val = dev.read(99999)
    return val.decode('utf-8').strip()
# End


def getinfo(stat):
    discard = []
    info = {'todo': [],}
    keys = {'V_0P55V': '0.55(V)', 'I_0P55V': '0.55(A)',
            'V_0P75V': '0.75(V)', 'I_0P75V': '0.75(A)',
            'V_1P10V': '1.15(V)', 'I_1P10V': '1.10(A)',
            'V_0P60V': '0.60(V)',
            'V_0P80V': '0.80(V)', 'I_0P80V': '0.80(A)',
            'V_12P0V': '12.0(V)', 'I_12P0V': '12.0(A)',
            'V_1P20V': '1.20(V)',
            'V_1P80V': '1.80(V)',
                                  'I_3P30V': '3.30(A)',
            'SakuraPower': 'Sakura',
            'InputPower':  'Input',
            'TMP1075':     'TI',
            'LTC7291':     'LTC',
            }
    s = stat
    s = s.replace('SAK Pwr', 'SakuraPower')
    s = s.replace('Inp Pwr', 'InputPower')
    s = s.replace('Now =', '')
    s = s.replace('Max =', '')
    s = s.replace(',    ', ',')
    s = s.replace(',   ', ',')
    s = s.replace(',  ', ',')
    s = s.replace(', ', ',')
    s = s.replace(':','=') 
    # print(s)
    # print('END')
    slist = s.split()
    found_equals = False
    for token in slist:
        if token.startswith('-') and token.endswith('-'):  # bunch of dashes
            pass
        elif token in keys:
            key = token
        elif token == '=':
            found_equals = True
        elif token in ['V','A','W','C']:
            units = token
            info[keys[key]] = [value, units]
            # unset for next line
            key = ''
            found_equals = False
            value = ''
            units = ''
        elif found_equals:
            value = token
        elif token in ['NOW', 'MAX', 'AVG']:  # discard column headers
            discard.append(token)
        elif token.startswith('(') and token.endswith(')'):  # discard counter
            discard.append(token)
        else:
            info['todo'].append(token)
    if len(discard) > 0:
        print('Discarding tokens: ' + ' '.join(discard))
    if len(info['todo']) > 0:
        print('Todo: ' + '\n'.join(info['todo']))
    else:
        del info['todo']
    return info
# End


def log(info):
    with open(os.path.join('log', logfile), 'a') as f:  # assumes 'log' folder exists
        f.write(info + '\n')
# End


def GetBestPort(thisfile):
    id_byfile = {
        '9182B':   ['10C4:EA60',],
        'statlog': ['0403:6015',],
        'help':    ['0403:6015',],  # copy of statlog id
        'snread':  ['0403:6015',],  # copy of statlog id
        'zmax':    ['0403:6015',],  # copy of statlog id
    }
    preferred = {  # first entry should be linux loopback, which will only show up if socat is running
        '9182B':   ['/home/ec/COM5', '/dev/ttyUSB91', 'COM91'],
        'statlog': ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51'],
        'help':    ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51'],  # copy of statlog ports
        'snread':  ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51'],  # copy of statlog ports
        'zmax':    ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51'],  # copy of statlog ports
    }
    goodports = []  # blank list that will contain ports that meet criteria
    try:
        id_list = id_byfile[thisfile]  # if this file has an entry, start with that list
        xx_list = preferred[thisfile]  # ditto
    except:
        if verbose:
            print('  Script filename not found in dict... ' + thisfile)  # default to S1LP/S2LP id
        id_list = ['0403:6015',]  # start with a list containing default
        xx_list = ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51',]  # ditto
    # add these lines to use windows null modem emulators
    # id_list.append('COM0COM')  # add null modem simulator for debug
    # id_list.append('ROOT\\PORTS')  # add null modem simulator for debug
    # xx_list.append('COM5')  # add null modem number for debug
    # xx_list.append('COM1')  # add null modem number for debug
    if verbose:
        print('  Valid ports must match ' + str(id_list))  # debug
        print('  Preferred ports order: ' + str(xx_list))  # debug
    for id in id_list:
        for portnum, portdesc, portdetails in serial.tools.list_ports.comports():
            if id in portdetails:  # check for MFG/product ID in details
                goodports.append(portnum)
                result = '  Found ' + id + ' in '
            else:
                result = '    ' + id + ' not in '
            if portdesc == 'n/a' and portdetails == 'n/a':  # u24 fix, tons of ports show up with no details
                pass
            else:  # port is real(ish) so display it
                if verbose:
                    print(result + portnum + ' | ' + portdesc + ' | ' + portdetails)
    if verbose:
        print('  Good Ports: ' + str(goodports))  # debug
    for port in xx_list:
        if port in goodports:  # requested port was found
            return port
    if len(goodports) > 0:  # at least one port matched target ID
        return goodports[0]
    return xx_list[0]  # no ports found, but return first preferred entry for linux simulation
    # linux doesn't find /home/username/whatever ports, just /dev/whatever, so the socat loopback never shows up
# End


def checkdir(dirname):
    try:
        os.mkdir(dirname)  # attempt to add folder
    except:
        pass  # folder exists, move on
# End


def GetCommand(fullfilename):
    global do_pause
    global do_slow
    global my_product
    global verbose

    # trim extension
    if fullfilename.endswith('.py'):
        thisfile = fullfilename[:-3]
    else:
        thisfile = fullfilename  # probably shouldn't be possible

    # strip -fast suffix
    if thisfile.endswith('-fast'):
        thisfile = thisfile[:-5]  # trim suffix
        do_pause = False

    # strip -void suffix
    if thisfile.endswith('-void'):
        thisfile = thisfile[:-5]  # trim suffix
        do_pause = False
        verbose = False

    # strip -null suffix
    if thisfile.endswith('-null'):
        thisfile = thisfile[:-5]  # trim suffix
        do_pause = False
        verbose = False
        null = True

    # strip -slow suffix
    if thisfile.endswith('-slow'):
        thisfile = thisfile[:-5]  # trim suffix
        do_slow = True

    # strip product prefix
    if thisfile.startswith('S1LP-'):
        thisfile = thisfile[5:]  # trim prefix
        my_product = 'S1LP'
    elif thisfile.startswith('S2LP-'):
        thisfile = thisfile[5:]  # trim prefix
        my_product = 'S2LP'
    elif thisfile.startswith('S2M2-'):
        thisfile = thisfile[5:]  # trim prefix
        my_product = 'S2M2'
    elif thisfile.startswith('S2XX-'):
        thisfile = thisfile[5:]  # trim prefix
        my_product = 'S2XX'

    # return command without prefix and suffix
    return thisfile.replace('.', ' ')  # replace dot with space

# End


def flags():
    # returns formatted string of all flags
    s = ''
    if do_pause == False:
        s = s + '[F]'
    if do_slow == True:
        s = s + '[S]'
    if verbose == True:
        s = s + '[V]'
    if null == True:
        s = s + '[N]'
    return s
# End


# start of script
if WINDOWS:
    msg = '\nDetected Windows OS\n'
elif LINUX:
    msg = '\nDetected linux OS\n'
else:
    msg = '\nUnknown OS\n'

# determine which command to send
if len(sys.argv) > 1:  # not just script name, but has arg(s)
    thisfile = GetCommand(' '.join(sys.argv[1:]))
else:  # use filename
    thisfile = GetCommand(os.path.basename(__file__))
if my_product in ['S1LP',]:  # list of products that use '?'
    help = '?'  # set to '?' for S1LP
else:
    help = 'help'  # set to 'help' for S2LP

if thisfile == 'statlog':  # default name in repo
    msg = msg + 'Logging stat command (' + my_product + ')'
    dostat = True
else:  # not statlog
    msg = msg + 'Sending command sequence to ' + my_product + flags() + ': ' + thisfile
    dostat = False
if verbose:  # have to wait until after filename is parsed to do first print check
    print(msg)

# set up logging
logfile = thisfile.replace(' ', '.') + '-' + hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
if verbose:
    print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
checkdir('log')  # just in case it doesn't exist, add it

# configure serial port and open connection
io = serial.Serial()
io.port = GetBestPort(thisfile)  # get best port option
io.baudrate = 115200
io.bytesize = 8
io.parity = 'N'
io.stopbits = 1
if do_pause == False:  # fast or void
    io.timeout = 0.2  # this might not always work, needs more testing
else:
    io.timeout = 1.0  # wait up to one second to read the stat command or whatever else is sent
# could add more flow control settings but they seem to default to off
if verbose:
    print('  Opening ' + io.port + ' (' + str(io.baudrate) + ',' + str(io.bytesize) + io.parity + str(io.stopbits) + ')')
else:
    void_msg = '[' + io.port + ']'  # start of message, command sequence to be added later
try:
    io.open()  # may succeed even if device is off
except:
    print('\n  Failed to open port...\n  Serial Number  = [Failed to open serial port]\n')  # trick snread script to extract a value
    sys.exit(0)

sn_dec = 'unknown'  # default in case it isn't read
if dostat:  # do not pause for input on the single commands, just the logging version
    s = other(io, 'snread')
    serial_line_start = s.find('Serial Number')
    serial_sub = s[serial_line_start + 15:]  # should be '= serdec = serhex...'
    serial_tokens = serial_sub.split()  # token index 1 and 3 will be serial number info
    sn_dec = serial_tokens[1]
    sn_hex = serial_tokens[3]
    print('Serial Number = ' + sn_dec + ' (' + sn_hex + ')')
    input("Press <Enter> to initiate logging...")
    print()
log('timestamp,S1LP SN ' + sn_dec + '...')  # header row

try:
    while True:
        t = int(time.time())  # floating point epoch time
        if dostat:
            s = stat(io)  # send stat command
        else:
            sequence = thisfile.split('+')  # plus sign may be used to separate commands
            if verbose == False:  # don't need to print for verbose mode, already done
                void_msg = void_msg + '  ' + str(sequence)  # add list containing command sequence to port info
            for command in sequence:
                newline = True  # print newline by default
                if command == 'help':  # encoded message, translates to '?' for S1LP
                    s = other(io, help)  # send question mark instead of the word help for S1LP
                else:
                    s = other(io, command)  # send ANY alternate command, so unsafe!
                s = s.replace('success 0x000000', ' ')  # strip verbosity
                # these should all be temporary!
                s = s.replace('TEMP_', '   T_')  # fix for S2LP stats for readability
                s = s.replace(' W_', ' P_')  # fix for S2LP stats for readability
                s = s.replace('I_P', ' I_')  # fix for S2LP stats for readability
                s = s.replace('I_CBLK', '  I_CB')  # fix for S2LP stats for readability
                s = s.replace('I_CB_A1A2', ' I_CB_A12')  # fix for S2LP stats for readability
                s = s.replace('I_CB_B1B2', ' I_CB_B12')  # fix for S2LP stats for readability
                # end of temporary replacements
                if s.startswith('Pin P'):  # S2 BMC verbose pin set output
                    slist = s[4:].split()  # split on all whitespace, starting with P after the word Pin
                    s = '\n' + ' '.join(slist) + '\n ' + slist[0][0:4]  # newline plus joined line plus pin number
                    newline = False
                if len(s) == 3:  # likely a stripped success message
                    newline = False
                if newline == False:
                    print(s, end='')  # print result without newline
                else:
                    print(s)  # print result
            if verbose == True:
                print()  # in case last result had no newline
            elif null:
                print()  # don't print any message
            else:
                print('  ' + void_msg)  # adds message to end of line
            break  # send alternate command sequence only once, immediately exit loop
        info = getinfo(s)
        # pprint.pprint(info)
        csv = []
        for k in info:
            row = k + ',' + info[k][0] + ',' + info[k][1]
            csv.append(row)
            print(row)
        if t - lastlog >= logdelay:  # wait at least logdelay seconds to write to log again
            lastlog = t  # record for subsequent checks
            log(','.join([ hex(t)[2:], ','.join(csv) ]))  # join with commas [timestamp, info]
        time.sleep(3)  # pause between reads
        print('\n------------- READING FROM SAKURA -------------\n')
except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
    print('\n  CTRL-C Detected')

if WINDOWS and do_pause:
    if do_slow:
        os.system('timeout /t 6')  # keep window open longer
    else:
        os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly        
elif LINUX and do_pause:
    os.system('sleep 2')  # pause for two seconds

#EOF

# NEED TO UPDATE FOR FTDI CHIP
# linux instructions for permanent port numbers
# create a file: 99-usb-serial.rules
# in folder: /etc/udev/rules.d/
# containing two lines:
# SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="ttyUSB91"
# EOT
# then do: udevadm control --reload-rules
# and then: reboot
