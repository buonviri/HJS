#!/bin/bash

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename: $hexstamp

# start card
cd ~/S1LP/install_mera/ && source start.sh && mera --sakura1_start

# make sure this was done once:
# cd ~/S1LP/inference/test/run_resnet50 && python3 deploy.py

# change to test folder
cd ~/S1LP/inference/test/run_resnet50

# store system info
echo -n "" > $hexstamp.info
sudo dmidecode --string baseboard-manufacturer | tee -a $hexstamp.info
sudo dmidecode --string baseboard-product-name | tee -a $hexstamp.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a $hexstamp.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a $hexstamp.info
uname -r | tee -a $hexstamp.info
powerprofilesctl get | tee -a $hexstamp.info

# run loop, pass timestamp as filename
for run in {1..60}; do
   python run_resnet50.py --target ip --log --csv_name $hexstamp --max_log 20 --forever --inference_freq 3
done
# 60 loops of 60 seconds: 1..60 in for loop, max_log 20, freq 3

# return to my folder
cd ~/HJS/u22

# EOF
