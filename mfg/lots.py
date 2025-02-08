# prints text, lot codess and SN ranges

import os
import re

location = '/home/ec/prodtest/'  # make this OS dependent eventually
prodtest = '^[0-9]{8}-.*\.txt$'  # must start with eight digits and a dash, then any random chars, with .txt extension at the end
info = {}  # blank dict for all lot code and serial number info

print()  # start with newline
print('Searching: ' + location)
print()  # separate with newline
for dirname, dirnames, filenames in os.walk(location):
    for filename in filenames:
        # print(filename)
        if re.match(prodtest, filename):
            lot = filename[0:5]
            sn = filename[5:8]
            snval = int(sn)
            # debug: print('lot = ' + lot + ' sn = ' + sn)
            if lot not in info:
                info[lot] = {}  # add empty dict
                info[lot]['min'] = snval
                info[lot]['max'] = snval
            try:
                info[lot][sn] = info[lot][sn] + 1  # attempt to increment counter then check min/max
                if snval < info[lot]['min']:
                    info[lot]['min'] = snval
                if snval > info[lot]['max']:
                    info[lot]['max'] = snval
            except:
                info[lot][sn] = 1  # start with counter of one
for lot in info:
    print(lot + ' ' + str(info[lot]['min']) + ' to ' + str(info[lot]['max']))  # print lot with min/max
    del info[lot]['min']  # remove min
    del info[lot]['max']  # remove max
    sns = []
    for sn in info[lot]:
        sns.append('  ' + sn + ' (runs=' + str(info[lot][sn]) + ')')  # store sn and count
    print('\n'.join(sorted(sns)))
print()

# EOF
