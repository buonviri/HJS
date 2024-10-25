#!/bin/bash

sudo dmesg | grep -i aspm | awk '{$1=$1;print}'
sudo lspci -s 01:00.0 -vvv | grep -i aspm | awk '{$1=$1;print}'
