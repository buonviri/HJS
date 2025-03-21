#!/bin/bash

function red () {
  printf "\e[1;31m%b\e[0m" "$1"
}

function green () {
  printf "\e[1;32m%b\e[0m" "$1"
}

# START OF SCRIPT
echo

if [ -d "/home/ec/hjs/" ]; then
  red "Output folder already exists. Overwriting...\n"
else
  green "Creating output folder...\n"
  mkdir -p "/home/ec/hjs/u22"
  mkdir -p "/home/ec/hjs/mfg"
  mkdir -p "/home/ec/hjs/statlog"
fi
cd "/home/ec/hjs/"

printf "\nAliases:\n"
foo="./.bash_aliases"  # new alias file
printf "# %s [%s]\n" "$(date)" "$(hostname)" > $foo  # start with date/time and hostname
cat "/home/ec/HJS/u22/edgecortix.bash_aliases" | grep -E ' s2i=| bios=| usbsn=| ver=| prodtest=| pt=| xlogver=| xlogslow=| xerr=| 1fdc=| s2=| info=| c008c=| dmadual=| dmasingle=| dryi=| dry=| enpg=| cfga=| cfgb=| cfg4pt=' | sed 's/\/HJS\//\/hjs\//g' | tee -a $foo

printf "\nScripts:\n"
yes | \cp -v /home/ec/HJS/u22/S2xx.sh ./u22/
yes | \cp -v /home/ec/HJS/u22/dma00d.sh ./u22/
yes | \cp -v /home/ec/HJS/u22/dma00s.sh ./u22/
yes | \cp -v /home/ec/HJS/statlog/statlog.py ./statlog/
yes | \cp -v /home/ec/HJS/mfg/prodtest.sh ./mfg/
yes | \cp -v /home/ec/HJS/mfg/cfg4pt.py ./mfg/

cd "/home/ec/HJS/"  # return to folder where this script exists
echo
# EOF
