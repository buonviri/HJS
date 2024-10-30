#!/bin/bash

# get bus info
echo
businfo="$(sudo lspci | grep 1fdc:0100 | head -c 7)"  # get first seven characters of the line that contains our ID
if [ -z "$businfo" ]; then  # check if empty
    printf "  1fdc:0100 not found\n  defaulting to 01:00.0\n\n"  # print error message
    businfo="01:00.0"  # set default
fi
echo Displaying info for: $businfo

# show card info
sudo lspci -vvv -s $businfo | grep -E --color=always "Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:" | awk '{$1=$1;print}'
echo

# EOF
