# prints text, lot codess and SN ranges

import os

for dirname, dirnames, filenames in os.walk(cat_letter):
    for filename in filenames:
        if filename.endswith('.txt'):
            print(filename)
# EOF
        