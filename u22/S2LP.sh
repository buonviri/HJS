#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
sleep 1
1fdc
sleep 1
cb12  # for S2LP
cd ~/S2LP/install_mera && source start.sh && cd ~/S2LP/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh

echo
mera --lssakura
echo

# end
