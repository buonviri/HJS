#!/bin/bash

if [ -d ~/mera_package/ ]; then
  mera="/home/ec/mera_package"
else
  mera="/home/ec/S2xx"
fi
echo path is $mera
echo arg is $1
fullpath=$mera/examples/$1
cd fullpath
chmod +x ./run.sh
./run.sh

# EOF
