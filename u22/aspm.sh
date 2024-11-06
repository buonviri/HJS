#!/bin/bash

echo

printf "\e[1;35mdmesg:\e[0m\n"
echo
sudo dmesg | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

printf "\e[1;35mlspci:\e[0m\n"
echo
sudo lspci -s 01:00.0 -vvv | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

# end

