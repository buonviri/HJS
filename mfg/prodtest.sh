#!/bin/bash
sudo echo # forces root login

# get timestamp, hexstamp, and hostname
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)  # echo "[DEBUG] timestamp: $hexstamp"
hostname=$(hostname)

# write timestamp
echo "[ProdTest on $hostname at UTC=0x$hexstamp] -> ~/.prodtest-$hexstamp" > ~/.prodtest-$hexstamp

# get serial number from FTDI
if [ -f ~/ftdi.info ]; then
  rm ~/ftdi.info  # remove existing file to be safe
fi
printf "\e[1;35m%b\e[0m" "   Reading FTDI serial number (lsusb)\n"
usbsn | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  USB serial number

# BMC: serial, version, PCIe
printf "\e[1;35m%b\e[0m"  "   Reading BMC serial number / version / PCIe status (info and srread 0xC008C) - "
info > ~/bmc.info
if [ $# == 1 ]; then  # any single arg works
  c008c-dual >> ~/bmc.info
else
  c008c >> ~/bmc.info
fi

cat ~/bmc.info | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  variants and revisions
cat ~/bmc.info | \grep -i -o -E "primary|secondary" || echo "Unknown"  # print one of three outcomes

# get serial number and card name
sn_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iSerial 3 \K.*")
sn_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P ".....-PAC..." | sed "s/-PAC//g")
id_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iProduct 2 FT230X on \K.*")
id_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board: EdgeCortix \K....")
dual=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board:.*variant \K...")  # should be D16 or S16

# cfg edit string
cfga > /dev/null
cfgb > /dev/null
cfg4pt >> ~/.prodtest-$hexstamp

# 1FDC:xxxx
printf "\e[1;35m%b\e[0m" "   Reading OS info (lspci - requires sudo)\n"
1fdc | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PCIe without leading spaces, uses sudo

# verify CB/PG
printf "\e[1;35m%b\e[0m" "   Reading CB info (BMC pins)\n"
enpg | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PG from BMC

# xlog
printf "\e[1;35m%b\e[0m"  "   Reading xlog...\n"
xlogver > ~/zog.info  # first half of xlog alias
xlogslow >> ~/zog.info  # second half of xlog alias
xerr | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # xlog pass/fail/error lines without leading spaces

# ant22/dryi and dma
printf "\e[1;35m%b\e[0m"  "   Running all DMA tests...\n"
bistfail=$(cat ~/.prodtest-$hexstamp | \grep -i "fail")
if [ -n "$bistfail" ]; then  # check if not empty
  printf "\e[1;31m%b\e[0m"  "   ABORTED DUE TO BIST FAILURE\n"
else
  cd ~/dna2_self_test_2_2_0/ > /dev/null  # setup must be run from the correct folder
  ./setup_3pg_none.sh > /dev/null 2>&1  # hide all of the spam, now skips dma_test
  cd - > /dev/null  # return to previous folder
  if [ "$dual" == "D16" ]; then
    dmadual >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, dual, S2LP
  else
    dmasingle >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, single, S2LP or S2M2
  fi
fi

# debug /00 issue
echo "HJS WAS HERE [NULL CHAR ISSUE]" >> ~/.prodtest-$hexstamp

# stats
s2 >> ~/.prodtest-$hexstamp

echo  # results
cat ~/.prodtest-$hexstamp

# rename based on serial number
if [ "${#sn_ftdi}" -eq 8 ] && [ "$sn_ftdi" == "$sn_bmc" ]; then
  printf "\e[1;32mVerify %s == %s \u2611\e[0m\n" $sn_ftdi $sn_bmc
  # printf "Lot Code: ${sn_bmc:0:5}\n"
  mkdir -p ~/prodtest/"${sn_bmc:0:5}"
  printf "HJS "  # signature prefix
  mv -v ~/.prodtest-$hexstamp ~/prodtest/"${sn_bmc:0:5}"/"$sn_bmc"-0x"$hexstamp".txt  # rename file
  sn_command=$(printf "sn %s %s" "${sn_bmc:0:5}" "${sn_bmc:5:8}")  # store serial number command
  printf "\nDisplay all stats using command: %s (SHIFT-CTRL-V ENTER)\n" "$sn_command"
  echo $sn_command | xsel -b  # copy to clipboard
  echo $sn_command > ~/.last_sn  # write to hidden file
else
  printf "\e[1;31mLength of serial number is incorrect or there is a mismatch: FTDI=$sn_ftdi BMC=$sn_bmc\e[0m\n"
fi

echo
# EOF
