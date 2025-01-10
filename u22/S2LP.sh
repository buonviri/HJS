#!/bin/bash

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cb12  # for S2LP
cd ~/S2xx/install_mera && source start.sh && cd ~/S2xx/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh

echo
mera --lssakura
echo

# end
