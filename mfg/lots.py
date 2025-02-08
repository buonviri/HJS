# prints text, lot codess and SN ranges

import os

location = '/home/ec/prodtest/'  # make this OS dependent eventually

print('Searching: ' + location)
for dirname, dirnames, filenames in os.walk(location):
    for filename in filenames:
        # print(filename)
        if filename.endswith('.txt'):
            print('Good' + filename)
# EOF
