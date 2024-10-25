#!/bin/bash

echo

echo dmesg:
echo
sudo dmesg | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

echo lspci:
echo
sudo lspci -s 01:00.0 -vvv | grep -i --color=always aspm | awk '{$1=$1;print}'

echo

# end

