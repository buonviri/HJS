from subprocess import Popen, PIPE

process = Popen(['lsusb'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
lsusb = stdout.decode("utf-8")

# print(lsusb)

devtypes = {'hub': [], 'mouse': [], 'keyboard': [], '802.11': [], 'uart': []}
misc = []

devices = lsusb.split('\n')
for device in devices:
    s = device.strip()
    # print(s)
    for devtype in devtypes:
        # print(devtype + ' --- ' + s)
        if devtype in s.lower():
            devtypes[devtype].append(s)
            s = ''
    if len(s) > 0:
        misc.append(s)

for devtype in devtypes:
    if len(devtypes[devtype]) > 0:  # only print ones with entries
        print('\n--- ' + devtype + ' ---')
        for line in devtypes[devtype]:
            bus_and_desc = line.split(':',1)
            print('  ' + '\n  '.join(bus_and_desc))
print()
if len(misc) > 0:
    print(misc)

