# prints text, lot codess and SN ranges

import os
import re

location = '/home/ec/prodtest/'  # make this OS dependent eventually
prodtest = '^[0-9]{8}-.*\.txt$'  # must start with eight digits and a dash, then any random chars, with .txt extension at the end

print('Searching: ' + location)
for dirname, dirnames, filenames in os.walk(location):
    for filename in filenames:
        # print(filename)
        if re.match(prodtest, filename):
            print(' ' + filename, end='')
# EOF
