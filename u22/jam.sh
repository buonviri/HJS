#!/bin/bash

# store command sequence, timestamp, hex timestamp
jamlog="$@"
jamt=$(date +%s)
jamhex=$(printf "%x" $jamt)

# store SN
sn_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iSerial 3 \K.*")  # copied from prodtest
if [ -z "$sn_ftdi" ]; then
  sn_ftdi="xxxxxyyy"
fi

# display info in terminal
echo Writing to file...
echo $jamhex
echo $sn_ftdi
echo $jamlog

# check if file exists, create if not
if [ ! -f ~/jam.info ]; then
    echo "Timestamps and log entries:" > ~/jam.info
fi

# write info to file
echo $jamhex $sn_ftdi $jamlog >> ~/jam.info

# EOF
