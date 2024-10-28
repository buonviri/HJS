# ports.py

import serial.tools.list_ports  # requires pip install pyserial
import os

for a,b,c in serial.tools.list_ports.comports():
    if b == 'n/a' and c == 'n/a':
        # print('N/A')
        pass
    else:
        print()
        print(a)
        print(b)
        print(c)

# pause if windows (in case it was run by double-clicking)
if os.name == 'nt':
    os.system('timeout /t 5')  # wait five seconds then close window or return to prompt

print()  # blank line

# end
