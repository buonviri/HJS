#!/bin/bash

# compare timestamps
echo Local and NIST time:
date '+%H:%M:%S'
ntpdate -q time.nist.gov | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
date '+%H:%M:%S'

# create new file or empty existing one
echo -n "" > ~/sys.info

# append lines with system info
sudo dmidecode --string baseboard-manufacturer | tee -a ~/sys.info
sudo dmidecode --string baseboard-product-name | tee -a ~/sys.info
# doesn't work in 20.04, suppress error
sudo dmidecode --string bios-revision 2> /dev/null | tee -a ~/sys.info
sudo dmidecode --string bios-version | tee -a ~/sys.info
lscpu | grep -Po 'Model name:\s+\K.*' | tee -a ~/sys.info
lsb_release -d | grep -Po 'Description:\s+\K.*' | tee -a ~/sys.info
uname -r | tee -a ~/sys.info
# doesn't work in 20.04, suppress error
powerprofilesctl get 2> /dev/null | tee -a ~/sys.info
python3 ~/HJS/statlog/snread-fast.py | grep -Po 'Serial Number  =\s+\K.*' | tee -a ~/sys.info

# EOF
