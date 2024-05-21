from subprocess import Popen, PIPE

def LogSystemInfo(filename):
    parameters = {
        'Board Vendor': ['cat', '/sys/devices/virtual/dmi/id/board_vendor'],
        'Board Name': ['cat', '/sys/devices/virtual/dmi/id/board_name'],
        'BIOS Release': ['cat', '/sys/devices/virtual/dmi/id/bios_release'],
        'BIOS Version': ['cat', '/sys/devices/virtual/dmi/id/bios_version'],
        
        
        'Kernel': ['uname', '-r'],
        'Power Profile': ['powerprofilesctl','get'],
    }

    for label in parameters:
        os_command = parameters[label]
        process = Popen(os_command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        info = stdout.decode("utf-8")
        print(label + ': ' + info.strip())
    return


LogSystemInfo('xxx')

# EOF

"""
cat /sys/devices/virtual/dmi/id/board_vendor | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/board_name | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/bios_release | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/bios_version | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
uname -r | tee -a ~/sys.info
# doesn't work in 20.04, suppress error
powerprofilesctl get 2> /dev/null | tee -a ~/sys.info
"""