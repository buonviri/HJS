#!/bin/bash

# compare timestamps
echo Local and NIST time:
date '+%H:%M:%S'
ntpdate -q time.nist.gov | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename: $hexstamp

# start card
cd ~/S1LP/install_mera/ && source start.sh && mera --sakura1_start

# change to test folder
cd ~/S1LP/inference/

# store system info
echo -n "" > $hexstamp.info
sudo dmidecode --string baseboard-manufacturer | tee -a $hexstamp.info
sudo dmidecode --string baseboard-product-name | tee -a $hexstamp.info
# u20 - skip bios-revision
sudo dmidecode --string bios-version | tee -a $hexstamp.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a $hexstamp.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a $hexstamp.info
uname -r | tee -a $hexstamp.info
# u20 - skip powerprofilescfg
# need consistent way to read S1LP SN

# run
python run_models.py --csv_name $hexstamp

# return to my folder
cd ~/HJS/u22

# EOF
