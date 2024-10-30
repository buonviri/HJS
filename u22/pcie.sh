#!/bin/bash

# get bus info
businfo="$(sudo lspci | grep 1fdc:0100 | head -c 7)"
if [ -z "$businfo" ]; then  # check if empty
    echo "1fdc:0100 not found; defaulting to 01:00.0"
    businfo="01:00.0"  # set default
fi
echo
echo Displaying info for: $businfo

# show card info
sudo lspci -vvv -s $businfo | grep -E --color=always "Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:" | awk '{$1=$1;print}'
echo

# EOF
