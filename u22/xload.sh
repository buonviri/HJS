#!/bin/bash

echo This process  may take up to a minute. Do not access the serial port until it completes.
echo

# set up picocom
picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0

# send xload 1 command
echo "xload 1" | picocom -qrix 1000 /dev/ttyUSB0

# send hex file
echo Sending hex file...
cat ./S112.hex | picocom -qrix 1000 /dev/ttyUSB0

echo

# End
