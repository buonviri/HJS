#!/bin/bash

# determine wait timer
if [ $# == 1 ]; then  # one arg was passed
  delay="$1"  # set to arg
else
  delay="5000"  # default
fi

function purple () {
  printf "\e[1;35m%b\e[0m" "$1"
}

# initial warning
echo
purple "This process may take a while. Do not access the serial port until it completes.\n"
echo

# set up picocom
picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0

# send bist command, wait up to 5 seconds for more data
echo "Delay =" $delay
echo "bist" | picocom -qrix $delay /dev/ttyUSB0

# hopefully it finished!
echo Done.
echo

# End
