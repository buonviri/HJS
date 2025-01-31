#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

echo
bmc
echo
1fdc
echo
# compute blocks now enabled in BMC
# cb12  # now works for both cards
# echo

cd ~/S2xx/install_mera && source start.sh && cd ~/S2xx/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
cd ~/S2xx

echo
mera --lssakura
echo

# end
