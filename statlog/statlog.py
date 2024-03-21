# Rev 0.00: started from 9182B.py

import serial  # requires pip install pyserial
import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir

import pprint  # temp

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

# set columns and rows in Windows
cols = 180
rows = 45

# set delay between log entries (in seconds)
logdelay = 3

# initialize log timer to 1970
lastlog = 0


def stat(dev):
    dev.write(b'stat\n')
    val = dev.read(9999)
    return val.decode('utf-8').strip()
# End


def OLDgetinfo(stat):
    s = stat.replace('---------------------------------------',' ') + ' '  # remove dashes and add trailing space
    lines = s.split('\n')
    s = ' '.join(lines)  # gets rid of CRLF
    # print('Oneline: '+ s)
    s = s.replace(' V ','|')
    s = s.replace(' A ','|')
    s = s.replace(' W ','|')
    s = s.replace(' C ','|')
    # print('Pipes: ' + s)
    slist = s.split('|')
    info = {}
    for x in slist:
        if '=' in x:
            kv = x.split('=')
            info[kv[0].strip()] = kv[1].strip()
        elif ':' in x:
            kv = x.split(':')
            info[kv[0].strip()] = kv[1].strip()
        elif len(x.strip()) > 0:
            print('Todo: ' + x.strip())
    print(info)
    return info
# End


def getinfo(stat):
    discard = []
    info = {'todo': [],}
    keys = ['V_0P55V', 'I_0P55V',
            'V_0P75V', 'I_0P75V',
            'V_1P10V', 'I_1P10V',
            'V_0P60V',
            'V_0P80V', 'I_0P80V',
            'V_12P0V', 'I_12P0V',
            'V_1P20V',
            'V_1P80V',
                       'I_3P30V',
            'SakuraPower',
            'InputPower',
            'TMP1075',
            'LTC7291',
            ]
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
    for token in slist:
        if token.startswith('-') and token.endswith('-'):  # bunch of dashes
            pass
        elif token in keys:
            key = token
        elif token == '=':
            found_equals = True
        elif token in ['V','A','W','C']:
            units = token
            info[key] = [value, units]
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
    print('Discarding: ' + ' '.join(discard))
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


# start of script
if WINDOWS:
    colsandrows = str(cols) + ',' + str(rows)
    os.system('mode ' + colsandrows)  # set window size in cols,rows maybe...
    print('\nDetected Windows OS\n')
    print('Attempting to set Cols,Rows to ' + colsandrows)  # works on win10, and maybe on win11 if conhost.exe is used?
else:
    print('\nDetected linux OS\n')

logfile = hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
try:
    os.mkdir('log')  # just in case it doesn't exist
except:
    pass  # folder exists, move on

# configure serial port and open connection
ec = serial.Serial()
if LINUX:  # check for linux
    ec.port = '/dev/ttyUSB51'  # expects serial port to be set to 91
    # to permanently set ttyUSB91, copy 99-usb-serial.rules to /etc/udev/rules.d/
    # run udevadm control --reload-rules then reboot
else:  # os.name is most likely 'nt' but no point in checking
    ec.port = 'COM51'  # note that this value must be set in Windows Device Manager
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

while True:
    t = int(time.time())  # floating point epoch time
    s = stat(ec)
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
            os.system('timeout /t 10')  # keep window open for up to ten seconds, keystroke ends it instantly
        elif LINUX:
            os.system('sleep 3')  # pause for three seconds
        break
    print('-------------------------------')

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
