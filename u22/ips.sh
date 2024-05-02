#!/bin/bash

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename: $hexstamp

# start card
cd ~/S1LP/install_mera/ && source start.sh && mera --sakura1_start

# change to test folder
cd ~/S1LP/inference/

# store system info (u20, skips bios-revision and powerprofilescfg)
echo -n "" > $hexstamp.info
sudo dmidecode --string baseboard-manufacturer | tee -a $hexstamp.info
sudo dmidecode --string baseboard-product-name | tee -a $hexstamp.info
sudo dmidecode --string bios-version | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a $hexstamp.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a $hexstamp.info
uname -r | tee -a $hexstamp.info

# run
python run_models.py --csv_name $hexstamp

# return to my folder
cd ~/HJS/u22

# EOF
