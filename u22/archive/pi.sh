#!/bin/bash

if [ $# == 1 ]; then  # one arg was passed
  cmd="$1"  # set command to arg
  echo "$cmd" | picocom -qrix 500 /dev/ttyUSB0  # send command
else  # no args were passed (or maybe 2+)
  picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0  # set up picocom
fi

# End
