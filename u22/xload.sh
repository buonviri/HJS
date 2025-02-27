#!/bin/bash

function purple () {
  printf "\e[1;35m%b\e[0m" "$1"
}

# initial warning
echo
purple "This process may take up to a minute. Do not access the serial port until it completes.\n"
echo

# set up picocom
picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0

# send xload 1 command
echo "xload 1" | picocom -qrix 1000 /dev/ttyUSB0

# send hex file
echo
echo "[Sending hex file]"
echo
cat ./S112.hex | picocom -qrix 1000 /dev/ttyUSB0

# requires poweroff
echo
echo Cycle power to boot the new image.
echo

# End
