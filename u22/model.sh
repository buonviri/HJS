#!/bin/bash

model=$1

# determine folder
if [ -d ~/mera_package/ ]; then
  mera="/home/ec/mera_package"
else
  mera="/home/ec/S2xx"
fi

# calculate path and display info
fullpath=$mera/examples/$model
printf "Running \e[1;32m%s\e[0m in [%s]\n\n" "$1" "$fullpath"

# run
cd $fullpath
chmod +x ./run.sh
./run.sh

# EOF
