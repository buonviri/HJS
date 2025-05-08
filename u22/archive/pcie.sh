#!/bin/bash

# this script is only useful for S1LP
# for S2LP use 1fdc instead

sudo echo  # ensure password has been entered, print blank line

# get bus info
businfo="$(sudo lspci | grep 1fdc:0100 | head -c 7)"  # get first seven characters of the line that contains our ID
if [ -z "$businfo" ]; then  # check if empty
    printf "  1fdc:0100 not found\n  defaulting to 01:00.0\n\n"  # print error message
    businfo="01:00.0"  # set default
fi
printf "\e[1;35mDisplaying info for: $businfo\e[0m\n"
echo

# show card info
sudo lspci -vvv -s $businfo | grep -E --color=always "Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:" | awk '{$1=$1;print}'

echo

# EOF
