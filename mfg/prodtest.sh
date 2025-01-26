#!/bin/bash

echo
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)

# DEBUG
# echo timestamp: $hexstamp
# END

# start
sudo echo [ProdTest $hexstamp] | tee ~/.prodtest-$hexstamp  # forces root login

# serial in FTDI
usbsn | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  #  USB serial number

# BMC: serial, version, PCIe
python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write BMC serial and version to file
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info
cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  #  variants and revisions

# 1fdc
1fdc | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  # PCIe without leading spaces

echo  # do not tee
# EOF
