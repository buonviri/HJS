#!/bin/bash

# get bus info
businfo="$(sudo lspci | grep 1fdc:0000 | head -c 7)"
echo
echo Displaying info for: $businfo

# show card info
sudo lspci -vvv -s $businfo | grep -E --color=always "Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:" | awk '{$1=$1;print}'
echo

# EOF
