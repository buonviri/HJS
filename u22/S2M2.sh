#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
sleep 1
1fdc
sleep 1
cbm2  # for S2M2
cd ~/S2M2/install_mera && source start.sh && cd ~/S2M2/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh

echo
mera --lssakura
echo

# end
