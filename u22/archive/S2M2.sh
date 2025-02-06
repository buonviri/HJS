#!/bin/bash

# changed S2xx to [home directory]

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cbm2  # for S2M2
cd ~/[home directory]/install_mera && source start.sh && cd ~/S2xx/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
cd ~/[home directory]

echo
mera --lssakura
echo

# end
