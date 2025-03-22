#!/bin/bash

# compare timestamps
printf "\e[1;35mUTC:\e[0m\n"
date --utc '+%H:%M:%S' | xargs printf "%s (local)\n"
cat </dev/tcp/time.nist.gov/13 | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]' | xargs printf "%s (NIST)\n"
date --utc '+%H:%M:%S' | xargs printf "%s (local)\n"
printf "\e[1;35m--------\e[0m\n"

# create new file or empty existing one
echo -n "" > ~/sys.info

# append lines with system info
hostname | tee -a ~/sys.info
foo=$(cat ~/sys.info | grep EC-RP)
if [ $? -eq 0 ]; then  # found RP
  cat /proc/device-tree/model | sed '$a\' | tee -a ~/sys.info  # rpi version has no newline
else
  cat /sys/devices/virtual/dmi/id/board_vendor | tee -a ~/sys.info
  printf " -> " | tee -a ~/sys.info  # indent
  cat /sys/devices/virtual/dmi/id/board_name | tee -a ~/sys.info
  cat /sys/devices/virtual/dmi/id/bios_version | tee -a ~/sys.info
  printf " -> " | tee -a ~/sys.info  # indent
  cat /sys/devices/virtual/dmi/id/bios_release | tee -a ~/sys.info
fi
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
printf " -> " | tee -a ~/sys.info  # indent
uname -r | tee -a ~/sys.info
# doesn't work in 20.04, suppress error
powerprofilesctl get 2> /dev/null | tee -a ~/sys.info

# check if S1LP
foo=$(lspci | grep 1fdc:0100)
if [ $? -eq 0 ]; then
    python3 ~/HJS/statlog/statlog.py S1LP-snread-fast | grep -Po 'Serial Number  =\s+\K.*' | tee -a ~/sys.info
else  # terminal only, not stored in sys.info
    echo No S1LP found.
fi

# check if S2LP/S2M2
foo=$(lspci | grep 1fdc:0001)
if [ $? -eq 0 ]; then
    python3 ~/HJS/statlog/statlog.py S2XX-cfg-fast | grep -Po 'Serial Number\s+=\s+\K.*' | tee -a ~/sys.info
else  # terminal only, not stored in sys.info
    echo No S2XX found.
fi

cd

# EOF
