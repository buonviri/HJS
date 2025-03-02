#!/bin/bash

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
purple "This process may take up to a minute. Do not access the serial port until it completes.\n"
echo

# change baud rate
python3 ~/HJS/statlog/statlog.py S2XX-baud.3 | \grep "baud "  # >> /dev/null

# set up picocom
picocom -qrX -b 345600 --flow x --send-cmd ascii-xfr /dev/ttyUSB0

# send xload 1 command
echo "xload 1" | picocom -qrix 1000 /dev/ttyUSB0

# send hex file
echo
echo "[Sending hex file $hexver.hex]"
echo
start=$(date +%s)
cat /home/ec/Downloads/$hexver.hex | picocom -qrix 1000 /dev/ttyUSB0
end=$(date +%s)
elapsed=$((end-start))

# change baud rate, requires br3x suffix
echo
python3 ~/HJS/statlog/statlog.py S2XX-baud.1-br3x | \grep "baud "  # >> /dev/null
echo "Transfer time = $elapsed s"

# requires poweroff
echo Cycle power to boot the new image.
echo

# play sound
aplay /home/ec/Music/440.wav --quiet

# End
