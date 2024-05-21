from subprocess import Popen, PIPE

def LogSystemInfo(filename):
    parameters = {
        'Board Vendor': ['cat', '/sys/devices/virtual/dmi/id/board_vendor'],
        'Board Name': ['cat', '/sys/devices/virtual/dmi/id/board_name'],
        'BIOS Release': ['cat', '/sys/devices/virtual/dmi/id/bios_release'],
        'BIOS Version': ['cat', '/sys/devices/virtual/dmi/id/bios_version'],
        'CPU': ['lscpu'],  # multi-line string that gets parsed later
        'OS': ['lsb_release', '-d'],  # string that gets split later
        'Kernel': ['uname', '-r'],
        'Power Profile': ['powerprofilesctl','get'],
    }

    for label in parameters:
        os_command = parameters[label]
        process = Popen(os_command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        info = stdout.decode("utf-8")
        if label == 'CPU':  # special case for lscpu
            lines = info.split('\n')
            for line in lines:
                if line.strip().startswith('Model name:'):
                    info = line[11:]  # skip the search string
        elif label == 'OS':  # special case for lsb_release
            line = info.split(None, 1)  # split only once, whitespace is likely tab
            info = line[1]  # right half of string
        label = label + ':'  # add colon before right-justify operation
        print(label.rjust(15) + '  ' + info.strip())
    return


LogSystemInfo('xxx')

# EOF
