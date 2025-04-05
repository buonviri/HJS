#!/bin/bash
sudo echo # forces root login

# get timestamp, hexstamp, and hostname
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)  # echo "[DEBUG] timestamp: $hexstamp"
hostname=$(hostname)

# write timestamp
echo "[ProdTest on $hostname at UTC=0x$hexstamp] -> ~/.prodtest-$hexstamp" > ~/.prodtest-$hexstamp

# change to prodtest bin
cd ~/prodtest/bin/

# get serial number from FTDI
ftdi=$(source ./ftdi.sh)
printf "\e[1;35m%b\e[0m%s\n" "   FTDI: " "$ftdi"
cat ~/prodtest/bin/bar-ftdi >> ~/.prodtest-$hexstamp

# get image location from BMC
nbmc=$(source ./info.sh)
printf "\e[1;35m%b\e[0m%s\n" "   nBMC: " "$nbmc"
cat ~/prodtest/bin/bar-info >> ~/.prodtest-$hexstamp

# cfg edit string
cfga > /dev/null
cfgb > /dev/null
cfg4pt >> ~/.prodtest-$hexstamp
cfg4pt_fail=$(cat ~/.prodtest-$hexstamp | \grep "MISSING")  # should be empty, matches indicate serial failure

# get serial number and card name
sn_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P ".....-PAC..." | sed "s/-PAC//g")  # SNSEP
id_ftdi=$(cat ~/prodtest/bin/bar-ftdi | \grep -o -P "iProduct 2 FT230X on \K.*")  # unused
id_bmc=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board: EdgeCortix \K....")
dual=$(cat ~/.prodtest-$hexstamp | \grep -o -P "Board:.*variant \K...")  # should be D16 or S16

# 1FDC:xxxx
printf "\e[1;35m%b\e[0m" "   Reading OS info (lspci - requires sudo) - "
1fdc | awk '{$1=$1;print}' > ~/.1fdc
pcie_status=$(cat ~/.1fdc | \grep -i -o -P 'Speed.*' || echo "Unknown")
echo $pcie_status | sed "s/) /) - /g" | sed "s/),/)/g"  # print after replacing some chars
cat ~/.1fdc >> ~/.prodtest-$hexstamp  # PCIe without leading spaces, requires sudo

# verify CB/PG
printf "\e[1;35m%b\e[0m" "   Reading CB info (BMC pins) - "
enpg > ~/.enpg
enpg_status=$(cat ~/.enpg | \grep -i -o -P ' 1 ' || echo "Unknown")
echo $enpg_status
cat ~/.enpg | \grep -E 'AEN|BEN|M2EN' | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # PG from BMC with only enable lines printed
enpg_fail=$(cat ~/.prodtest-$hexstamp | \grep -E 'AEN|BEN|M2EN')  # should not be empty

# xlog
printf "\e[1;35m%b\e[0m"  "   Reading xlog...\n"
xlogver > ~/zog.info  # first half of xlog alias
xlogslow >> ~/zog.info  # second half of xlog alias
xerr | awk '{$1=$1;print}' >> ~/.prodtest-$hexstamp  # xlog pass/fail/error lines without leading spaces

# ant22/dryi and dma
printf "\e[1;35m%b\e[0m"  "   Running all DMA tests...\n"
bistfail=$(cat ~/.prodtest-$hexstamp | \grep -i "fail")
if [ -n "$bistfail" ]; then  # check if not empty
  printf "\e[1;31m%b\e[0m"  "   ABORTED DUE TO BOOT/BIST/TEST FAILURE\n"
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

# ./bmc test, requires driver to be installed
qbmc > ~/.qbmc
qbmc_result=$(cat ~/.qbmc | \grep -i "bmcrevision" || echo "Failed to read BMC Revision")  # either read string or report error
printf "./bmc [bin] -> $qbmc_result\n" >> ~/.prodtest-$hexstamp

# debug /00 issue
echo "HJS WAS HERE [NULL CHAR ISSUE]" >> ~/.prodtest-$hexstamp

# stats
s2 >> ~/.prodtest-$hexstamp

echo  # results
cat ~/.prodtest-$hexstamp

# rename based on serial number
if [ -n "$cfg4pt_fail" ]; then  # check if not empty
  printf "\n\e[1;31mSerial Failure during cfg4pt\e[0m\n"
elif [ -z "$enpg_fail" ]; then  # check if empty
  printf "\n\e[1;31mSerial Failure during enpg\e[0m\n"
elif [ "${#ftdi}" -eq 8 ] && [ "$ftdi" == "$sn_bmc" ]; then
  printf "\e[1;32mVerify %s == %s \u2611\e[0m\n" $ftdi $sn_bmc
  # printf "Lot Code: ${sn_bmc:0:5}\n"
  mkdir -p ~/prodtest/"${sn_bmc:0:5}"
  printf "HJS "  # signature prefix
  mv -v ~/.prodtest-$hexstamp ~/prodtest/"${sn_bmc:0:5}"/"$sn_bmc"-0x"$hexstamp".txt  # rename file
  sn_command=$(printf "sn %s %s" "${sn_bmc:0:5}" "${sn_bmc:5:8}")  # store serial number command
  printf "\nDisplay all stats using command: %s (SHIFT-CTRL-V ENTER) or the alias \"last\"\n" "$sn_command"
  echo $sn_command | xsel -b  # copy to clipboard
  echo $sn_command > ~/.last_sn  # write to hidden file
else
  printf "\n\e[1;31mLength of serial number is incorrect or there is a mismatch: FTDI=$ftdi BMC=$sn_bmc\e[0m\n"
fi

echo
# EOF
