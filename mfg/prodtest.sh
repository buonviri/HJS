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
info > ~/bmc.info
c008c >> ~/bmc.info
cat ~/bmc.info | grep -i -E "variant|revision|c008c" | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  #  variants and revisions

# get serial number and card name
sn_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iSerial 3 \K.*")
sn_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P ".....-PAC..." | sed "s/-PAC//g")
id_ftdi=$(cat ~/.prodtest-$hexstamp | \grep -o -P "iProduct 2 FT230X on \K.*")
id_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board: EdgeCortix \K....")
dual=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board:.*variant \K...")  # should be D16 or S16

# 1FDC:xxxx
printf "\e[1;35m%b\e[0m" "   Reading OS info (lspci)\n"
1fdc | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PCIe without leading spaces

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
  printf "\e[1;35m%b\e[0m"  "   ABORTED DUE TO BIST FAILURE\n"
else
  cd ~/dna2_self_test_2_2_0/ > /dev/null  # setup must be run from the correct folder
  ./setup_3pg.sh > /dev/null 2>&1  # hide all of the spam
  cd - > /dev/null  # return to previous folder
  if [ "$dual" == "D16" ]; then
    dmadual >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, dual, S2LP
  else
    dmasingle >> ~/.prodtest-$hexstamp  # run all DMA tests using version with minimal spam, single, S2LP or S2M2
  fi
fi

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
else
  printf "\e[1;31mLength of serial number is incorrect or there is a mismatch: FTDI=$sn_ftdi BMC=$sn_bmc\e[0m\n"
fi

echo
# EOF
