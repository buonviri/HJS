#!/bin/bash

# compare timestamps
echo Local/NIST/Local time:
date '+%H:%M:%S'
ntpdate -q time.nist.gov | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
date '+%H:%M:%S'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename: $hexstamp

# store system info (now done in sensorsj)
# cd ~/S1LP/inference/log/
# echo -n "" > $hexstamp.info
# cat /sys/devices/virtual/dmi/id/board_vendor | tee -a $hexstamp.info
# cat /sys/devices/virtual/dmi/id/board_name | tee -a $hexstamp.info
# cat /sys/devices/virtual/dmi/id/bios_release | tee -a $hexstamp.info
# cat /sys/devices/virtual/dmi/id/bios_version | tee -a $hexstamp.info
# lscpu | grep -Po 'Model name:\s+\K.*' | tee -a $hexstamp.info
# lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a $hexstamp.info
# uname -r | tee -a $hexstamp.info
# doesn't work in 20.04, suppress error
# powerprofilesctl get 2> /dev/null | tee -a $hexstamp.info
# S1LP SN is now read by statlog so this method is no longer required:
# python3 ~/HJS/statlog/snread-fast.py | grep -Po 'Serial Number  =\s+\K.*' | tee -a $hexstamp.info
# cd "$OLDPWD"

# start card
cd ~/S1LP/install_mera/
source start.sh
mera --sakura1_start
cd "$OLDPWD"

# change to test folder, run, return to previous folder
cd ~/S1LP/inference/
python run_models.py --csv_name $hexstamp
cd "$OLDPWD"

# EOF
