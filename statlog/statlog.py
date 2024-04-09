# Rev 0.00: started from 9182B.py
# Rev 1.00: first integrated release
# Rev 1.01: better COM port management
# Rev 1.02: initialize found_equals which didn't matter until
#           it ran on linux mint for some reason

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

# default ports and ID for linux and windows
serialports = {'posix': '/dev/ttyUSB51', 'nt': 'COM51'}
ecid = '0403:6015'


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


def GetBestPort(port, id):
    goodports = []  # list of ports that meet criteria
    for portnum, portdesc, portdetails in serial.tools.list_ports.comports():
        if id in portdetails:  # check for MFG/product ID in details
            goodports.append(portnum)
            print('  Found: ' + portnum)
            print('  Desc = ' + portdesc)
            print('  Details = ' + portdetails)
        # else:  # debug
        #     print('  A: ' + portnum)
        #     print('  B = ' + portdesc)
        #     print('  C = ' + portdetails)
    if port in goodports:  # requested port was found
        return port
    elif len(goodports) > 0:  # at least one port matched target ID
        return goodports[0]
    elif 'COM0COM' in portdetails:  # windows null modem app connecting COM5 and COM6
        print('  Null Modem Mode for HJS')
        return('COM5')
    else:
        return 'NONE'  # no ports found
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
thisfile = os.path.basename(__file__).split('.')[0]  # get script name
if thisfile == 'statlog':
    print('Logging stat command')
    dostat = True
else:
    if thisfile == '((help))':  # encoded message
        thisfile = '?'  # replace verbose filename with brief serial command
    print('Sending single command: ' + thisfile)
    dostat = False

# set up logging
logfile = hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
checkdir('log')  # just in case it doesn't exist, add it

# configure serial port and open connection
ec = serial.Serial()
ec.port = serialports[os.name]  # this will raise an exception if os.name isn't recognized
print('  Preferred port is: ' + ec.port)
ec.port = GetBestPort(ec.port, ecid)  # use <ec.port, ecid> for operation, <'COM5', COM0COM> for simulation
ec.baudrate = 115200
ec.bytesize = 8
ec.parity = 'N'
ec.stopbits = 1
ec.timeout = 1  # wait up to one second to read
# could add more flow control settings but they seem to default to off
try:
    ec.open()  # may succeed even if device is off
except:
    print('\n  Simulation mode\n')  # not actually implemented

input("Press <Enter> to initiate logging...")

while True:
    t = int(time.time())  # floating point epoch time
    if dostat:
        s = stat(ec)  # send stat command
    else:
        s = other(ec, thisfile)  # send other command, so unsecure!
        print(s)
        break
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
    try:  # normal operation
        time.sleep(3)  # pause between reads
    except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
        print('\n  CTRL-C Detected')
        if WINDOWS:
            os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly
        elif LINUX:
            os.system('sleep 2')  # pause for two seconds
        break
    print('\n------------- READING FROM SAKURA -------------\n')

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
