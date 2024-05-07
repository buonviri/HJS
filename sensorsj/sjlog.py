# Rev 0.00: copied from 9182B

import time    # need time.time, time.sleep
import os      # need os.system, os.mkdir
from subprocess import Popen, PIPE
from ast import literal_eval
import yaml

# pseudo #defines
WINDOWS = os.name == 'nt'
LINUX = os.name == 'posix'

# set delay between log entries (in seconds)
logdelay = 1

# initialize log timer to 1970
lastlog = 0


def log(info):
    with open(os.path.join('log', logfile), 'a') as f:  # assumes 'log' folder exists
        f.write(info + '\n')
# End


def checkdir(dirname):
    try:
        os.mkdir(dirname)  # attempt to add folder
    except:
        pass  # folder exists, move on
# End


# start of script
if WINDOWS:
    print('\nDetected Windows OS\n')
elif LINUX:
    print('\nDetected linux OS\n')
else:
    print('\nUnknown OS\n')
try:
    with open('sjscan.yaml', 'r') as f: 
        cfg = yaml.safe_load(f)
    print('Logging:')
    for k in cfg['A) Fan Speed']:
        print(k)
    for k in cfg['B) Temperature']:
        print(k)
    print()
except:
    print('Run sjscan.py to generate a sensor list!')
    cfg = {}  # blank sensor list if no yaml
# print(cfg)  # debug

checkdir('log')  # just in case it doesn't exist, add it
logfiletime = int(time.time())  # int version of current time
logfile = hex(logfiletime)[2:] + '.csv'  # epoch time in hex (minus the 0x prefix) with csv extension
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))

try:
    fdata = []  # blank list of fan sensor readings
    tdata = []  # blank list of temperature sensor readings
    while True:
        t = int(time.time())  # floating point epoch time converted to int
        # sensors -j returns multi-line formatted JSON
        process = Popen(["sensors", "-j"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        sensors = stdout.decode("utf-8")
        sjdict = literal_eval(sensors)
        for k in cfg['A) Fan Speed']:
            try:
                fdata.append(sjdict[k[0]][k[1]][k[2]])
            except:
                fdata.append(-999)  # error reading sensor
        for k in cfg['B) Temperature']:
            try:
                tdata.append(sjdict[k[0]][k[1]][k[2]])
            except:
                tdata.append(-999)  # error reading sensor
        if t - lastlog >= logdelay:  # wait at least logdelay seconds to write to log again
            lastlog = t  # record for subsequent checks
            log(','.join([hex(t)[2:],'data goes here']))  # join with commas [timestamp, Tmin, Tmax, fans...]
            print(hex(t)[2:] + ' ... ')
            print(fdata)
            print(tdata)
            print()
            fdata = []  # clear
            tdata = []  # clear
        time.sleep(0.3)  # allows 3-4 reads per second
except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
    print('\n  CTRL-C Detected')

if WINDOWS:
    os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly
elif LINUX:
    os.system('sleep 2')  # pause for two seconds

#EOF
