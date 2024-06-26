# Rev 0.00: experimental only
# Rev 1.00: works on linux

import serial  # requires pip install pyserial
import serial.tools.list_ports
import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

# default ports
serialports = {'linux': '/home/ec/COM6', 'windows': 'COM6'}

# number format for voltage, current, power
format = '%0.3f'


def rand():
    random = str(time.time())  # get current time as string with lots of decimal places
    srandom = random[-4:-1]  # skip the last char, use the next three (-4 -3 -2)
    return float(srandom) / 1000  # divide by 1000 to get a value between 0 and 1
# End


# 9182B simulation
def id9182(dev):
    val = b'Fake 9182B ID String\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def maxv9182(dev):
    val = b'12.345\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def on9182(dev):
    print('Turning Device On, No Response Expected')
def v9182(dev):
    fval = 11 + rand()*2  # floating point value
    sval = format % fval  # string version
    val = bytes(sval + '\n', 'utf-8')
    # val = b'11.000\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def i9182(dev):
    fval = 1 + rand()*4  # floating point value
    sval = format % fval  # string version
    val = bytes(sval + '\n', 'utf-8')
    # val = b'1.000\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
# End


# S1LP simulation
def sakstat(dev):
    fval = 0.50 + rand()*10/100  # 0.50 to 0.60
    sval = format % fval  # string version
    val = bytes('V_0P55V = ' + sval + ' V\n', 'utf-8')
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def sakzmax(dev):
    val = b'Zeroing Max Values\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def saksn(dev):
    val = b'SN = 12345\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
def sakhelp(dev):
    val = b'S1LP Help\n'
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
# End


# Host USB simulation
def hostsj(dev):
    val = b"""{'x': 'This will contain sensors -j info'}\n"""
    print('Writing: ' + val.decode('utf-8').strip())
    dev.write(val)
# End


def log(info):
    with open(os.path.join('log', logfile), 'a') as f:  # assumes 'log' folder exists
        f.write(info + '\n')
# End


# start of script

# OS info
if WINDOWS:
    print('\nDetected Windows OS\n')
elif LINUX:
    print('\nDetected linux OS\n')
else:
    print('\nUnknown OS\n')

devinfo = {  # commands and response functions, also baudrate setting
    '9182': {'baudrate': '57600', '*IDN?': id9182, 'SOUR:VOLT?': maxv9182, 'OUT:ALL 1': on9182, 'MEAS:VOLT?': v9182, 'MEAS:CURR?': i9182},
    'S1LP': {'baudrate': '115200', 'stat': sakstat, 'zmax': sakzmax, 'snread': saksn, '?': sakhelp},
    'host': {'baudrate': '115200', 'sensorsj': hostsj, 'sj': hostsj},
    # add more devices here as needed
    'auto': {'baudrate': '115200'}
    }
dev = 'S1LP'  # manually set the device type
thisfile = os.path.basename(__file__).split('.')[0][3:]  # get script name without extension, starting at fourth char (skip sm- prefix)
if thisfile in devinfo:  # check if script has been renamed to match a devinfo key
    dev = thisfile  # override dev
# set dictionary to be used in loop
if dev == 'auto':
    responses = {}  # need to make loop and add all
elif dev in devinfo:
    responses = devinfo[dev]
else:
    responses = {}  # invalid selection
# print(responses)  # debug
print('Device = ' + dev)

logfile = hex(int(time.time()))[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
try:
    os.mkdir('log')  # just in case it doesn't exist
except:
    pass  # folder exists, move on

# configure serial port and open connection
ec = serial.Serial()
if LINUX:  # check for linux
    ec.port = serialports['linux']
else:  # os.name is most likely 'nt' but no point in checking
    ec.port = serialports['windows']
print('  Preferred port is: ' + ec.port)
# try to determine port name automatically
for portnum, portdesc, portdetails in serial.tools.list_ports.comports():
    if 'ROOT\\PORTS' in portdetails:  # Shareware name
        ec.port = portnum
        print('  Found: ' + portnum)
        print('  Desc = ' + portdesc)
        print('  Details = ' + portdetails)
    elif portdesc == 'n/a' and portdetails == 'n/a':  # u24 fix, tons of ports show up with no details
        pass
    else:
        print('  Found: ' + portnum)
        print('  Desc = ' + portdesc)
        print('  Details = ' + portdetails)
ec.baudrate = int(devinfo[dev]['baudrate'])
ec.bytesize = 8
ec.parity = 'N'
ec.stopbits = 1
ec.timeout = 1  # wait to read, should be ignored if \n is found, but does not for some reason
# could add more flow control settings but they seem to default to off

tzero = int(time.time())  # record start time
tlast = tzero
try:
    print('  Opening: ' + ec.port)
    ec.open()  # may succeed even if device is off
    while True:
        if ec.in_waiting:  # bytes exist in buffer
            data = ec.readline()  # can wait up to one second to get all bytes
            command = data.decode('utf-8').strip()
            print(command.rjust(20) + ' -> ', end="")
            log(command)
            try:
                responses[command](ec)  # call the function and pass it the device
            except:
                print('Unknown command')
        else:
            t = int(time.time())  # floating point epoch time
            if t > tlast:  # at least one second has passed
               print('[' + str(t-tzero) + ']')
               tlast = t  # don't print for at least another second
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nExiting (CTRL-C)...')
    time.sleep(3)
except:
    print('\nExiting (Unknown Error)...')
    time.sleep(10)  # allow time to read error on screen

#EOF
