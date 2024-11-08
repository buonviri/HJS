#!/bin/bash

sudo echo  # ensure password has been entered, print blank line

printf "\e[1;35m'ASPM' in dmesg:\e[0m\n"
echo
sudo dmesg | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

printf "\e[1;35m'ASPM' in lspci:\e[0m\n"
echo
sudo lspci -vvv -d 1fdc:0100 | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

# end

