#!/bin/bash

echo

printf "\e[1;35mASPM in dmesg:\e[0m\n"
echo
sudo dmesg | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

printf "\e[1;35mASPM in lspci:\e[0m\n"
echo
sudo lspci -vvv -d 1fdc:0100 | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

# end

