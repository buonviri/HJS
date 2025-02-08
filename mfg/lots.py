# prints text, lot codess and SN ranges

import os

for dirname, dirnames, filenames in os.walk('~/prodtest/'):
    for filename in filenames:
        if filename.endswith('.txt'):
            print(filename)
# EOF
        