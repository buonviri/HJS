#!/bin/bash

echo
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)

# DEBUG
# echo timestamp: $hexstamp
# END

sudo echo [ProdTest $hexstamp] | tee ~/.prodtest-$hexstamp  # forces root login

python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc | tee -a ~/.prodtest-$hexstamp  # write info to file
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc | tee -a ~/.prodtest-$hexstamp  # append PCIe info

# DEBUG
# echo
# echo [ALL]
# echo
# cat ~/.bmc  # debug, dislplay file
# echo
# echo [/ALL]
# echo
# END

cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  #  variants and revisions
usbsn | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  #  USB serial number

# DEBUG
1fdc | awk '{$1=$1;print}' | tee -a ~/.prodtest-$hexstamp  # PCIe without leading spaces
# END

echo  # do not tee
# EOF
