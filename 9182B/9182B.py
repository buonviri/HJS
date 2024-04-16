# Rev 0.00: prints one P=IV reading and exits
# Rev 0.01: toggle on/off implemented
# Rev 1.00: infinite loop with CTRl-C to exit
# Rev 1.01: added graph
# Rev 1.02: added simulation mode
# Rev 1.03: fake random numbers
# Rev 1.04: added timeout after CTRL-C
# Rev 1.05: updated comments, ready for release
# Rev 1.06: added nt vs posix options
# Rev 1.10: first integrated release
# Rev 1.11: better COM port management
# Rev 1.20: com port choice improved

import serial  # requires pip install pyserial
import serial.tools.list_ports
import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

# set columns and rows in Windows
cols = 180
rows = 45

# set delay between log entries (in seconds)
logdelay = 1

# initialize log timer to 1970
lastlog = 0

# choose graphing character:
# 0x2587 is 7/8 height rectangle, didn't exist in font used in Win10 command prompt
# 0x2588 is full height rectangle, works but is too much white
# 0x23 is pound sign
# 0x7C is pipe
rect = chr(0x7C)

# number format for voltage, current, power
format = '%0.3f'


def identify(dev):
    dev.write(b'*IDN?\n')
    val = dev.readline()
    return val.decode("utf-8").strip()
# End


def voltagemax(dev):  # same as using Vset button
    dev.write(b'SOUR:VOLT?\n')
    val = dev.readline()
    return val.decode("utf-8").strip()
# End


def voltage(dev):
    dev.write(b'MEAS:VOLT?\n')
    val = dev.readline()
    return val.decode("utf-8").strip()
# alt function:
def simvoltage(dev):  # use this when not connected
    val = 11 + rand()*2
    return format % val
# End


def current(dev):
    dev.write(b'MEAS:CURR?\n')
    val = dev.readline()
    return val.decode("utf-8").strip()
# alt function:
def simcurrent(dev):  # use this when not connected
    val = 1 + rand()*4
    return format % val
# End


def power(i,v):
    power = float(i) * float(v)
    return format % power  # string formatted with decimal places
# End


def on(dev):
    dev.write(b'OUT:ALL 1\n')
# alt function:
def simon(dev):
    print('Enabling Power')
# End


def off(dev):
    dev.write(b'OUT:ALL 0\n')
# End


def log(info):
    with open(os.path.join('log', logfile), 'a') as f:  # assumes 'log' folder exists
        f.write(info + '\n')
# End


def rand():
    random = str(time.time())  # get current time as string with lots of decimal places
    srandom = random[-4:-1]  # skip the last char, use the next three (-4 -3 -2)
    return float(srandom) / 1000  # divide by 1000 to get a value between 0 and 1
# End


def GetBestPort():
    id_byfile = {
        '9182B': ['10C4:EA60',],
        'statlog': ['0403:6015',],
        # new null modem cable is '0403:6001', could be used for sermon and its children
    }
    preferred = {  # first entry should be linux loopback, which will only show up if socat is running
        '9182B': ['/home/ec/COM5', '/dev/ttyUSB91', 'COM91'],
        'statlog': ['/home/ec/COM5', '/dev/ttyUSB51', 'COM51'],
    }
    goodports = []  # blank list that will contain ports that meet criteria
    thisfile = os.path.basename(__file__).split('.')[0]  # get filename (minus extension) for possible match
    try:
        id_list = id_byfile[thisfile]  # if this file has an entry, start with that list
        xx_list = preferred[thisfile]  # ditto
    except:
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
            if portdesc == 'n/a' and portdetails == 'n/a':  # u24 fix, tons of ports show up with no details
                pass
            else:  # port is real(ish) so display it
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

logfile = hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
checkdir('log')  # just in case it doesn't exist, add it

# configure serial port and open connection
io = serial.Serial()
io.port = GetBestPort()  # get best port option
io.baudrate = 57600
io.bytesize = 8
io.parity = 'N'
io.stopbits = 1
io.timeout = 1  # wait up to one second to read
# could add more flow control settings but they seem to default to off
fn = [simvoltage,simcurrent,simon]  # default to simulation mode
print('  Opening ' + io.port + ' (' + str(io.baudrate) + ',' + str(io.bytesize) + io.parity + str(io.stopbits) + ')')
try:
    io.open()  # may succeed even if device is off
    id = identify(io)  # get ID
    if id == '':  # timeout (device off or not connected) results in empty string
        print('Device not found\n')
    else:
        print('Device = ' + id + '\n')
        # display Voltage Setting
        vmax = voltagemax(io)
        print('Vset = ' + vmax + ' V\n')
        fn = [voltage,current,on]  # override simulation mode with real functions
except:
    print('Simulation mode\n')

input("Press <Enter> to enable power and initiate logging...")
fn[2](io)  # enable power, function #2

try:
    while True:
        t = int(time.time())  # floating point epoch time converted to int
        v = fn[0](io)    # read voltage, function #0, depends on simulation mode
        i = fn[1](io)    # read current, function #1, depends on simulation mode
        p = power(i,v)   # power, multiplies current and voltage
        nz = float(p)+1  # get non-zero value of power
        rects = int(nz)  # get int for multiplying string, range should be 1 to ceiling(max)
        print('  ' + v + ' V' + ' x ' + i + ' A' + ' = ' + p.rjust(7) + ' W  ' + rect*rects)  # rjust accounts for 100+ watts
        if t - lastlog >= logdelay:  # wait at least logdelay seconds to write to log again
            lastlog = t  # record for subsequent checks
            log(','.join([hex(t)[2:],p,i,v]))  # join with commas [timestamp, power, current, voltage]
        time.sleep(0.3)  # loop should happen twice per second, possibly three times
except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
    print('\n  CTRL-C Detected')

if WINDOWS:
    os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly
elif LINUX:
    os.system('sleep 2')  # pause for two seconds

#EOF
