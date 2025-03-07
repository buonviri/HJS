#!/bin/bash

# store command sequence, timestamp, hex timestamp
allargs="$@"
dectime=$(date +%s)
hextime=$(printf "%x" $dectime)

# get serial number from FTDI
if [ -f ~/ftdi.info ]; then  # if file exists
  rm ~/ftdi.info  # remove existing file to be safe
fi
usbsn > /dev/null  # writes USB serial number to file with no output

# echo debug:
# cat ~/ftdi.info | grep iSerial

sn_ftdi=$(cat ~/ftdi.info | \grep -o -P "iSerial.*3.*\K[0-9]{8}")  # get eight digit decimal version
# echo SN=$sn_ftdi
if [ -z "$sn_ftdi" ]; then
  sn_ftdi="xxxxxyyy"  # default value
fi

# display info in terminal
echo "Writing to file @$hextime"
echo "SN $sn_ftdi"
echo "$allargs"

# check if file exists, create if not
if [ ! -f ~/jam.info ]; then
    echo "Timestamps and log entries:" > ~/jam.info
fi

# write info to file
echo $hextime $sn_ftdi $allargs >> ~/jam.info

# EOF
