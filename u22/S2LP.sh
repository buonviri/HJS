#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cb12  # for S2LP
cd ~/S2LP/install_mera && source start.sh && cd ~/S2LP/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
mera --lssakura

echo

# end
