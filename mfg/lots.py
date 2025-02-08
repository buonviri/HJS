# prints text, lot codess and SN ranges

import os

location = '~/prodtest/'  # make this OS dependent eventually

print('Searching: ' + location)
for dirname, dirnames, filenames in os.walk(location):
    for filename in filenames:
        if filename.endswith('.txt'):
            print(filename)
# EOF
        