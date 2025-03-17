#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

# determine folder
if [ -d ~/mera_package/ ]; then
  mera="/home/ec/mera_package"  # use $HOME instead?
else
  mera="/home/ec/S2xx"  # this is only here to support legacy installations
fi

echo
bmc
echo
1fdc
echo
# compute blocks now enabled in BMC
# cb12  # now works for both cards
# echo

cd $mera/install_mera && source start.sh && cd $mera/initialize_sakura_ii && chmod +x ./setup_3pg_none.sh && ./setup_3pg_none.sh
cd $mera

echo
mera --lssakura
echo

# end
