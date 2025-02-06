#!/bin/bash

if [ -d ~/mera_package/ ]; then
  mera="~/mera_package"
else
  mera="~/S2xx"
fi
echo $mera
echo $1
cd $mera/examples/$1 && chmod +x ./run.sh && ./run.sh

# EOF
