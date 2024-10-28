# ports.py

import serial.tools.list_ports  # requires pip install pyserial
import os

for a,b,c in serial.tools.list_ports.comports():
    print()
    print(a)
    print(b)
    print(c)

# assumes windows! FIX IT
os.system('timeout /t 5')  # wait five seconds then close window or return to prompt

# end
