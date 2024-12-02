#!/bin/bash

# store command sequence, timestamp, hex timestamp
jamlog="$@"
jamt=$(date +%s)
jamhex=$(printf "%x" $jamt)

# display info in terminal
echo Writing to file...
echo $jamhex
echo $jamlog

# check if file exists, create if not
if [ ! -f ~/jam.info ]; then
    echo "Timestamps and log entries:" > ~/jam.info
fi

# write info to file
echo $jamhex $jamlog >> ~/jam.info

# EOF
