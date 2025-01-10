#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cbm2  # for S2M2
cd ~/S2M2/install_mera && source start.sh && cd ~/S2M2/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
mera --lssakura

echo

# end
