#!/bin/bash

# determine folder
if [ -d ~/mera_package/ ]; then
  mera="/home/ec/mera_package"  # use $HOME instead?
else
  mera="/home/ec/S2xx"  # this is only here to support legacy installations
fi

cd $mera/install_mera
source start.sh
cd $mera
mera --lssakura

# end
