# ports.py

import serial.tools.list_ports  # requires pip install pyserial

for a,b,c in serial.tools.list_ports.comports():
    print(a)
    print(b)
    print(c)


