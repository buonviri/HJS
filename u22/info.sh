#!/bin/bash

# compare timestamps
printf "\e[1;35mLocal and NIST time:\e[0m\n"
date '+%H:%M:%S'
ntpdate -q time.nist.gov | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
date '+%H:%M:%S'
printf "\e[1;35m--------\e[0m\n"

# create new file or empty existing one
echo -n "" > ~/sys.info

# append lines with system info
hostname | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/board_vendor | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/board_name | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/bios_release | tee -a ~/sys.info
cat /sys/devices/virtual/dmi/id/bios_version | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
uname -r | tee -a ~/sys.info
# doesn't work in 20.04, suppress error
powerprofilesctl get 2> /dev/null | tee -a ~/sys.info
python3 ~/HJS/statlog/snread-fast.py | grep -Po 'Serial Number  =\s+\K.*' | tee -a ~/sys.info

# EOF
