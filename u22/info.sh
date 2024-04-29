#!/bin/bash

# create new file or empty existing one
echo -n "" > ~/sys.info

# append lines with system info
sudo dmidecode --string baseboard-manufacturer | tee -a ~/sys.info
sudo dmidecode --string baseboard-product-name | tee -a ~/sys.info
sudo dmidecode --string bios-revision | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
uname -r | tee -a ~/sys.info
powerprofilesctl get | tee -a ~/sys.info
python3 ~/HJS/statlog/snread.py | grep -Po 'Serial Number  =\s+\K.*' | tee -a ~/sys.info

# EOF
