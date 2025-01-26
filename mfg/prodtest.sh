#!/bin/bash

echo  # get timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
logfile="~/.prodtest-$hexstamp"
# echo timestamp: $hexstamp

# write timestamp
sudo echo [ProdTest UTC $hexstamp] > logfile  # forces root login

# serial in FTDI
printf "\e[1;35m%b\e[0m" "   Reading FTDI serial number (lsusb)\n"
usbsn | awk '{$1=$1;print}' >> logfile  #  USB serial number

# BMC: serial, version, PCIe
printf "\e[1;35m%b\e[0m"  "   Reading BMC serial number / version / PCIe status (info and srread 0xC008C)\n"
python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write BMC serial and version to file
python3 ~/HJS/statlog/statlog.py S2XX-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info
cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' >> logfile  #  variants and revisions

# 1FDC
printf "\e[1;35m%b\e[0m" "   Reading OS info (lspci)\n"
1fdc | awk '{$1=$1;print}' >> logfile  # PCIe without leading spaces

# ant22 and dma
printf "\e[1;35m%b\e[0m"  "   Running all DMA tests...\n"
cd ~/S2LP/dna2_self_test_2_2_0/ > /dev/null  # setup must be run from the correct folder
./setup_3pg.sh > /dev/null 2>&1  # hide all of the spam
cd - > /dev/null  # return to previous folder
source ~/HJS/u22/dma00.sh >> logfile  # run all DMA tests using version with minimal spam

# xlog
printf "\e[1;35m%b\e[0m"  "   Reading xlog...\n"
python3 ~/HJS/statlog/statlog.py S2XX-ver-null > ~/zog.info  # first half of xlog alias
python3 ~/HJS/statlog/statlog.py S2XX-xlog-slow >> ~/zog.info  # second half of xlog alias
xerr | awk '{$1=$1;print}' >> logfile  # xlog pass/fail/error lines without leading spaces

# stats
s2 >> logfile

echo  # results
cat logfile

# validate serial number and card name
sn_ftdi=$(cat .prodtest-67965a8a | \grep -o -P "iSerial 3 \K.*")
sn_bmc=$(cat .prodtest-67965a8a | \grep -o -P ".....-PAC..." | sed "s/-PAC//g")
id_ftdi=$(cat .prodtest-67965a8a | \grep -o -P "iProduct 2 FT230X on \K.*")
id_bmc=$(cat .prodtest-67965a8a | \grep -o -P "Board: EdgeCortix \K....")
if [ "${#sn_ftdi}" -eq 8 ] && [ "$sn_ftdi" -eq "$sn_bmc" ]; then
  mv $logfile ~/sn_bmc-$hexstamp  # rename file
else
  echo "Length of serial number is incorrect or there is a mismatch: FTDI=$sn_ftdi BMC=$sn_bmc"
fi

# EOF
