#!/bin/bash

# store command sequence, timestamp, hex timestamp
jamlog="$@"
jamt=$(date +%s)
hexstamp=$(printf "%x" $jamt)

# get serial number from FTDI, copied from prodtest
if [ -f ~/ftdi.info ]; then
  rm ~/ftdi.info  # remove existing file to be safe
fi
usbsn  # writes USB serial number to file
sn_ftdi=$(cat ~/ftdi.info | \grep -o -P "iSerial 3 \K.*")
if [ -z "$sn_ftdi" ]; then
  sn_ftdi="xxxxxyyy"
fi

# display info in terminal
echo Writing to file...
echo $hexstamp
echo $sn_ftdi
echo $jamlog

# check if file exists, create if not
if [ ! -f ~/jam.info ]; then
    echo "Timestamps and log entries:" > ~/jam.info
fi

# write info to file
echo $hexstamp $sn_ftdi $jamlog >> ~/jam.info

# EOF
