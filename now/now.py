import os
import time
project = 'S2LP_'
extension = '.xlsx'
print(project + hex(int(time.time()))[2:].upper() + extension)
os.system('PAUSE')
