#!/bin/bash

baud="230400"
baudx="2"
undo="br2x"
folder="hex"  # default, may get overwritten
hexver="S115"  # default, update as needed

if [ $# == 1 ]; then  # one arg was passed
  hexver="$1"  # set to arg, overwrite default version
  if [ "$hexver" == "-d" ]; then  # special case, debug
    folder="hex-debug"
    hexver="xload"
  fi
fi

function red () {
  printf "\e[1;31m%b\e[0m" "$1"
}

function purple () {
  printf "\e[1;35m%b\e[0m" "$1"
}

# initial warning
echo
purple "This process may take up to a minute. Do not access the serial port until it completes.\n"
echo

# change baud rate
python3 ~/HJS/statlog/statlog.py S2XX-baud.$baudx | \grep "baud "  # >> /dev/null

# set up picocom
if [ -e /dev/ttyUSB0 ]; then
  picocom -qrX -b $baud --flow x --send-cmd ascii-xfr /dev/ttyUSB0
else
  red "/dev/ttyUSB0 is not connected"
fi

# send xload 1 command
if [ -e /dev/ttyUSB0 ]; then
  echo "xload 1" | picocom -qrix 1000 /dev/ttyUSB0
fi

# send hex file
start=$(date +%s)
if [ -e /dev/ttyUSB0 ]; then
  echo
  echo "[Sending file $folder/$hexver.hex]"
  echo
  cat /home/ec/hex-ftdi-cfg/$folder/$hexver.hex | picocom -qrix 1000 /dev/ttyUSB0
fi
end=$(date +%s)
elapsed=$((end-start))

# change baud rate, requires br3x suffix
echo
python3 ~/HJS/statlog/statlog.py S2XX-baud.1-$undo | \grep "baud "  # >> /dev/null
echo "Transfer time = $elapsed s"

# requires poweroff
if [ -e /dev/ttyUSB0 ]; then
  echo Cycle power to boot the new image.
fi
echo

# play sound
a440

# End
