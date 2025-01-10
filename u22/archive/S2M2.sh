#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cbm2  # for S2M2
cd ~/S2xx/install_mera && source start.sh && cd ~/S2xx/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
cd ~/S2xx

echo
mera --lssakura
echo

# end
