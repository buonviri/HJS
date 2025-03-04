#!/bin/bash

# reserved for future use
if [ $# == 1 ]; then  # one arg was passed
  hexver="$1"  # set to arg
else
  hexver="S112"  # default
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

# send bist command
echo "bist" | picocom -qrix 500 /dev/ttyUSB0
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist
bist=$(echo "" | picocom -qrix 500 /dev/ttyUSB0)
echo $bist

# hopefully it finished!
echo Done.
echo

# End
