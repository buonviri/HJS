#!/bin/bash

# store command sequence, timestamp, hex timestamp
allargs="$@"
dectime=$(date +%s)
hextime=$(printf "%x" $dectime)

# get serial number from FTDI
if [ -f ~/ftdi.info ]; then  # if file exists
  rm ~/ftdi.info  # remove existing file to be safe
fi
usbsn  # writes USB serial number to file
sn_ftdi=$(cat ~/ftdi.info | \grep -o -P "iSerial 3 \K.*")
if [ -z "$sn_ftdi" ]; then
  sn_ftdi="xxxxxyyy"
fi

# display info in terminal
echo Writing to file...
echo $hextime
echo $sn_ftdi
echo $jamlog

# check if file exists, create if not
if [ ! -f ~/jam.info ]; then
    echo "Timestamps and log entries:" > ~/jam.info
fi

# write info to file
echo $hextime $sn_ftdi $allargs >> ~/jam.info

# EOF
