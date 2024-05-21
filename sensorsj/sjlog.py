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


def LogSystemInfo():
    parameters = {  # note: keys may NOT contain commas
        'Board Vendor': ['cat', '/sys/devices/virtual/dmi/id/board_vendor'],
        'Board Name': ['cat', '/sys/devices/virtual/dmi/id/board_name'],
        'BIOS Release': ['cat', '/sys/devices/virtual/dmi/id/bios_release'],
        'BIOS Version': ['cat', '/sys/devices/virtual/dmi/id/bios_version'],
        'CPU': ['lscpu'],  # multi-line string that gets parsed later
        'OS': ['lsb_release', '-d'],  # string that gets split later
        'Kernel': ['uname', '-r'],
        'Power Profile': ['powerprofilesctl','get'],
    }
    csvfile = ''
    for label in parameters:
        try:
            os_command = parameters[label]
            process = Popen(os_command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            info = stdout.decode("utf-8")
        except:  # likely the command failed
            info = '[unknown]'
        if label == 'CPU':  # special case for lscpu
            lines = info.split('\n')
            for line in lines:
                if line.strip().startswith('Model name:'):
                    info = line[11:]  # skip the search string
        elif label == 'OS':  # special case for lsb_release
            line = info.split(None, 1)  # split only once, whitespace is likely tab
            info = line[1]  # right half of string
        info = info.strip()  # make sure it doesn't have extra whitespace
        if ',' in info:  # requires quotes
            csvinfo = '"' + info + '"'  # add quotes
        else:
            csvinfo = info  # leave as is
        csvfile = csvfile + label + ',' + csvinfo + '\n'
        label = label + ':'  # add colon before right-justify operation
        print(label.rjust(16) + '  ' + info)
    with open(os.path.join('log', sysinfofile), 'w') as f:  # assumes 'log' folder exists
        f.write(csvfile)
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
thisfile = os.path.basename(__file__).split('.')[0]  # get filename (minus extension) for possible match

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

hextimestamp = hex(int(time.time()))[2:]  # epoch time in hex (minus the 0x prefix)
sysinfofile = 'sysinfo-' + hextimestamp + '.csv'
logfile = thisfile + '-' + hextimestamp + '.csv'
print ('Logging to: ' + logfile + ' in ' + os.path.join(os.getcwd(), 'log'))
checkdir('log')  # just in case it doesn't exist, add it
LogSystemInfo()  # writes sys.info to sysinfofile
log('timestamp,Fmin,Fmax,Tmin,Tmax')  # create header row in log

try:
    fdata = []  # blank list of fan sensor readings
    tdata = []  # blank list of temperature sensor readings
    while True:
        t = int(time.time())  # floating point epoch time converted to int
        # sensors -j returns multi-line formatted JSON
        if LINUX:
            process = Popen(["sensors", "-j"], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            sensors = stdout.decode("utf-8")
            sjdict = literal_eval(sensors)
        else:
            sjdict = {"FakeDevice":{"Adapter":"FakeAdapter","fan1":{"fan1_input":1234.500,"fan1_pulses":2},"SYSTIN":{"temp1_input": 12.345},"NC":{"temp2_input": 123.45}}}
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
            svals = [hex(t)[2:],  # timestamp
                str(min(fdata, default=0)),  # default accounts for no fan data
                str(max(fdata, default=0)),  # default accounts for no fan data
                str(min(tdata)),
                str(max(tdata)),
                ]  # vals converted to strings
            log  (','.join(svals))  # join with commas [timestamp, fan min/max, temp min/max]
            print(' '.join(svals))  # print with spaces instead of commas
            # print(fdata)  # debug
            # print(tdata)  # debug
            # print()  # debug
            fdata = []  # clear
            tdata = []  # clear
        time.sleep(0.05)  # many reads per second, is this really necessary?
except KeyboardInterrupt:  # hitting CTRL-C will exit the script cleanly
    print('\n  CTRL-C Detected')

if WINDOWS:
    os.system('timeout /t 2')  # keep window open for up to two seconds, keystroke ends it instantly
elif LINUX:
    os.system('sleep 2')  # pause for two seconds

#EOF
