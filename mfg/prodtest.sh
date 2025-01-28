#!/bin/bash
echo

# get timestamp and hexstamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)  # echo "[DEBUG] timestamp: $hexstamp"

# write timestamp
sudo echo "[ProdTest UTC=0x$hexstamp] -> ~/.prodtest-$hexstamp" > ~/.prodtest-$hexstamp  # forces root login

# get serial number from FTDI
if [ -f ~/ftdi.info ]; then
  rm ~/ftdi.info  # remove existing file to be safe
fi
printf "\e[1;35m%b\e[0m" "   Reading FTDI serial number (lsusb)\n"
usbsn | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  USB serial number

# BMC: serial, version, PCIe
printf "\e[1;35m%b\e[0m"  "   Reading BMC serial number / version / PCIe status (info and srread 0xC008C)\n"
python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write BMC serial and version to file
python3 ~/HJS/statlog/statlog.py S2XX-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info
cat ~/.bmc | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  variants and revisions

# get serial number and card name
sn_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iSerial 3 \K.*")
sn_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P ".....-PAC..." | sed "s/-PAC//g")
id_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iProduct 2 FT230X on \K.*")
id_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board: EdgeCortix \K....")
dual=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board:.*variant \K...")  # should be D16 or S16

# 1FDC
printf "\e[1;35m%b\e[0m" "   Reading OS info (lspci)\n"
1fdc | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PCIe without leading spaces

# xlog
printf "\e[1;35m%b\e[0m"  "   Reading xlog...\n"
python3 ~/HJS/statlog/statlog.py S2XX-ver-null > ~/zog.info  # first half of xlog alias
python3 ~/HJS/statlog/statlog.py S2XX-xlog-slow >> ~/zog.info  # second half of xlog alias
xerr | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # xlog pass/fail/error lines without leading spaces

# ant22 and dma
printf "\e[1;35m%b\e[0m"  "   Running all DMA tests...\n"
bistfail=$(cat ~/.prodtest-$hexstamp | \grep -i "pass")
if [ bistfail ]; then
  printf "\e[1;35m%b\e[0m"  "   ABORTED DUE TO BIST FAILURE\n"
else
  cd ~/S2LP/dna2_self_test_2_2_0/ > /dev/null  # setup must be run from the correct folder
  ./setup_3pg.sh > /dev/null 2>&1  # hide all of the spam
  cd - > /dev/null  # return to previous folder
  if [ "$dual" == "D16" ]; then
    source ~/HJS/u22/dma00d.sh >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, dual
  else
    source ~/HJS/u22/dma00s.sh >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, single
  fi
fi

# stats
s2 >> ~/.prodtest-$hexstamp

echo  # results
cat ~/.prodtest-$hexstamp

# rename based on serial number
if [ "${#sn_ftdi}" -eq 8 ] && [ "$sn_ftdi" == "$sn_bmc" ]; then
  printf "Verify %s == %s \u2611\n" $sn_ftdi $sn_bmc
  printf "HJS "  # signature prefix
  mv -v ~/.prodtest-$hexstamp ~/$sn_bmc-0x$hexstamp.txt  # rename file
else
  echo "Length of serial number is incorrect or there is a mismatch: FTDI=$sn_ftdi BMC=$sn_bmc"
fi

echo
# EOF
