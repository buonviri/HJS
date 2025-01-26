#!/bin/bash

echo  # get timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
# echo timestamp: $hexstamp

# write timestamp
sudo echo [ProdTest UTC $hexstamp] > ~/.prodtest-$hexstamp  # forces root login

# serial in FTDI
echo Reading FTDI serial number...
usbsn | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  USB serial number

# BMC: serial, version, PCIe
echo
echo [get BMC serial, version, PCIe]
python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write BMC serial and version to file
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info
cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  #  variants and revisions

# 1FDC
echo
echo [get linux version of PCIe]
1fdc | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  # PCIe without leading spaces

echo  # do not tee

echo [---TEMP---]
cat ~/.prodtest-$hexstamp

# EOF
