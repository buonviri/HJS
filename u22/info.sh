#!/bin/bash

# create new file or empty existing one
echo -n "" > filename

# append lines with system info
sudo dmidecode --string baseboard-manufacturer | tee -a ~/sys.info
sudo dmidecode --string baseboard-product-name | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
uname -r | tee -a ~/sys.info
powerprofilesctl get | tee -a ~/sys.info

# EOF
