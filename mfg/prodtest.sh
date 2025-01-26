#!/bin/bash

echo  # get timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
# echo timestamp: $hexstamp

# write timestamp
sudo echo [ProdTest UTC $hexstamp] > ~/.prodtest-$hexstamp  # forces root login

# serial in FTDI
printf "Reading FTDI serial number (lsusb)\n"
usbsn | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  USB serial number

# BMC: serial, version, PCIe
printf "Reading BMC serial number / version / PCIe status (info and srread 0xC008C)\n"
python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write BMC serial and version to file
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info
cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  variants and revisions

# 1FDC
printf "Reading OS info (lspci)\n"
1fdc | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PCIe without leading spaces

echo  # results
cat ~/.prodtest-$hexstamp

# EOF
