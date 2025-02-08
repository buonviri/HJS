# prints text, lot codess and SN ranges

import os
import re

location = '/home/ec/prodtest/'  # make this OS dependent eventually
prodtest = '^[0-9]{8}-.*\.txt$'  # must start with eight digits and a dash, then any random chars, with .txt extension at the end
info = {}  # blank dict for all lot code and serial number info

print('Searching: ' + location)
for dirname, dirnames, filenames in os.walk(location):
    for filename in filenames:
        # print(filename)
        if re.match(prodtest, filename):
            lot = filename[0:5]
            sn = filename[5:8]
            print('lot = ' + lot + ' sn = ' + sn)
            if lot not in info:
                info[lot] = {}  # add empty dict
            try:
                info[lot][sn] = info[lot][sn] + 1  # attempt to increment counter
            except:
                info[lot][sn] = 1  # start with counter of one
print(info)
# EOF
