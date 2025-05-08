#!/bin/bash

sudo echo  # ensure password has been entered, print blank line

printf "\e[1;35m'ASPM' in dmesg:\e[0m\n"
echo
sudo dmesg | GREP_COLORS='ms=01;32' grep -i -E --color=always 'aspm=|aspm' | awk '{$1=$1;print}'

echo

printf "\e[1;35m'ASPM' in lspci:\e[0m\n"
echo
sudo lspci -vvv -d 1fdc: | GREP_COLORS='ms=01;32' grep -i -E --color=always 'aspm=|aspm' | awk '{$1=$1;print}'

echo

# end

