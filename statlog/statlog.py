# Rev 0.00: started from 9182B.py
# Rev 1.00: first integrated release
# Rev 1.01: better COM port management
# Rev 1.02: initialize found_equals which didn't matter until
#           it ran on linux mint for some reason
# Rev 1.03: added alternate commands
# Rev 1.20: com port choice improved

import serial  # requires pip install pyserial
import serial.tools.list_ports
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


def stat(dev):
    dev.write(b'stat\n')
    val = dev.read(9999)
    return val.decode('utf-8').strip()
# End


def other(dev, cmd):
    dev.write(bytes(cmd + '\n', 'utf-8'))
    val = dev.read(9999)
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


def GetBestPort():
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
    thisfile = os.path.basename(__file__).split('.')[0]  # get filename (minus extension) for possible match
    try:
        id_list = id_byfile[thisfile]  # if this file has an entry, start with that list
        xx_list = preferred[thisfile]  # ditto
    except:
        print('  Script filename not found in dict... ' + thisfile)  # debug
        id_list = ['script filename not found in list',]  # start with a list containing an invalid entry
        xx_list = ['script filename not found in list',]  # ditto
    id_list.append('COM0COM')  # add null modem simulator for debug
    id_list.append('ROOT\\PORTS')  # add null modem simulator for debug
    xx_list.append('COM5')  # add null modem number for debug
    xx_list.append('COM1')  # add null modem number for debug
    print('  Valid ports must match ' + str(id_list))  # debug
    print('  Preferred ports order: ' + str(xx_list))  # debug
    for id in id_list:
        for portnum, portdesc, portdetails in serial.tools.list_ports.comports():
            if id in portdetails:  # check for MFG/product ID in details
                goodports.append(portnum)
                result = '  Found ' + id + ' in '
            else:
                result = '    ' + id + ' not in '
            print(result + portnum + ' | ' + portdesc + ' | ' + portdetails)
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


# start of script
if WINDOWS:
    colsandrows = str(cols) + ',' + str(rows)
    os.system('mode ' + colsandrows)  # set window size in cols,rows maybe...
    print('\nDetected Windows OS\n')
    print('Attempting to set Cols,Rows to ' + colsandrows)  # works on win10, and maybe on win11 if conhost.exe is used?
elif LINUX:
    print('\nDetected linux OS\n')
else:
    print('\nUnknown OS\n')

# determine which command to send
thisfile = os.path.basename(__file__).split('.')[0]  # get script name without extension
if thisfile == 'statlog':  # default name in repo
    print('Logging stat command')
    dostat = True
else:
    if thisfile == 'help':  # encoded message, translates to '?'
        thisfile = '?'  # replace filename with brief serial command
    print('Sending single command: ' + thisfile)
    dostat = False

# set up logging
logfile = hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
checkdir('log')  # just in case it doesn't exist, add it

# configure serial port and open connection
io = serial.Serial()
io.port = GetBestPort()  # get best port option
io.baudrate = 115200
io.bytesize = 8
io.parity = 'N'
io.stopbits = 1
io.timeout = 1  # wait up to one second to read
# could add more flow control settings but they seem to default to off
print('  Opening ' + io.port + ' (' + str(io.baudrate) + ',' + str(io.bytesize) + io.parity + str(io.stopbits) + ')')
try:
    io.open()  # may succeed even if device is off
except:
    print('\n  Simulation mode\n')  # not actually implemented

if dostat:  # do not pause for input on the single commands, just the logging version
    input("Press <Enter> to initiate logging...")

try:
    while True:
        t = int(time.time())  # floating point epoch time
        if dostat:
            s = stat(io)  # send stat command
        else:
            s = other(io, thisfile)  # send alternate command, so unsafe!
            print(s)  # print result
            break  # send alternate command only once, immediately exit loop
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

if WINDOWS:
    os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly
elif LINUX:
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
