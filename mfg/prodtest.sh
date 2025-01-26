#!/bin/bash

sudo echo [ProdTest]  # forces root login

python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc  # write info to file
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc  # append PCIe info

# DEBUG
echo
echo [ALL]
echo
cat ~/.bmc  # debug, dislplay file
echo
echo [/ALL]
echo
# END

cat ~/.bmc | grep -i -E "variant|revision|c008c"  #  variants and revisions

# EOF
