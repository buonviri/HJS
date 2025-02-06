#!/bin/bash

# changed S2xx to [home directory]

sudo echo PCIe status, compute blocks, etc...

bmc
1fdc
cb12  # for S2LP
cd ~/[home directory]/install_mera && source start.sh && cd ~/[home directory]/initialize_sakura_ii && chmod +x ./setup.sh && ./setup.sh
cd ~/[home directory]

echo
mera --lssakura
echo

# end
