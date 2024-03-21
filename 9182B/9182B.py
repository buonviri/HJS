# Rev 0.00: prints one P=IV reading and exits
# Rev 0.01: toggle on/off implemented
# Rev 1.00: infinite loop with CTRl-C to exit
# Rev 1.01: added graph
# Rev 1.02: added simulation mode
# Rev 1.03: fake random numbers
# Rev 1.04: added timeout after CTRL-C
# Rev 1.05: updated comments, ready for release
# Rev 1.06: added nt vs posix options

import serial  # requires pip install pyserial
import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir

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
bk = serial.Serial()
if LINUX:  # check for linux
    bk.port = '/dev/ttyUSB91'  # expects serial port to be set to 91
    # to permanently set ttyUSB91, copy 99-usb-serial.rules to /etc/udev/rules.d/
    # run udevadm control --reload-rules then reboot
else:  # os.name is most likely 'nt' but no point in checking
    bk.port = 'COM91'  # note that this value must be set in Windows Device Manager
bk.baudrate = 57600
bk.bytesize = 8
bk.parity = 'N'
bk.stopbits = 1
bk.timeout = 1  # wait up to one second to read
# could add more flow control settings but they seem to default to off
fn = [simvoltage,simcurrent]  # default to simulation mode
try:
    bk.open()  # may succeed even if device is off
    id = identify(bk)  # get ID
    if id == '':  # timeout (device off or not connected) results in empty string
        print('\n  Device not found\n')
    else:
        print('\n  Device = ' + id + '\n')
        # display Voltage Setting
        vmax = voltagemax(bk)
        print('  Vset = ' + vmax + ' V')
        fn = [voltage,current]  # override simulation mode with real functions
except:
    print('\n  Simulation mode\n')

while True:
    t = int(time.time())  # floating point epoch time
    v = fn[0](bk)    # voltage, function #0, depends on simulation mode
    i = fn[1](bk)    # current, function #1, depends on simulation mode
    p = power(i,v)   # power, multiplies current and voltage
    nz = float(p)+1  # get non-zero value of power
    rects = int(nz)  # get int for multiplying string, range should be 1 to ceiling(max)
    print('  ' + v + ' V' + ' x ' + i + ' A' + ' = ' + p.rjust(7) + ' W  ' + rect*rects)  # rjust accounts for 100+ watts
    if t - lastlog >= logdelay:  # wait at least logdelay seconds to write to log again
        lastlog = t  # record for subsequent checks
        log(','.join([hex(t)[2:],p,i,v]))  # join with commas [timestamp, power, current, voltage]
    try:  # normal operation
        time.sleep(0.49)  # loop should happen twice per second
    except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
        print('\n  CTRL-C Detected')
        if WINDOWS:
            os.system('timeout /t 10')  # keep window open for up to ten seconds, keystroke ends it instantly
        elif LINUX:
            os.system('sleep 3')  # pause for three seconds
        break

#EOF

# linux instructions for permanent port numbers
# create a file: 99-usb-serial.rules
# in folder: /etc/udev/rules.d/
# containing two lines:
# SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="ttyUSB91"
# EOT
# then do: udevadm control --reload-rules
# and then: reboot
