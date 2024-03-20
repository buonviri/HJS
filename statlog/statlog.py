# Rev 0.00: started from 9182B.py

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


def stat(dev):
    dev.write(b'stat\n')
    val = dev.readline()
    return val.decode("utf-8").strip()
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
    print('\n  Simulation mode\n')

print(stat(ec))

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
