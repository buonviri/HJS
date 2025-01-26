#!/bin/bash

sudo echo [ProdTest]  # forces root login


python3 ~/HJS/statlog/statlog.py S2XX-info-void > ~/.bmc
python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void >> ~/.bmc

echo
echo [ALL]
cat ~/.bmc  # debug, dislplay file
echo [/ALL]
echo

cat ~/.bmc | grep -i -E "variant|revision"  #  variants and revisions

# EOF
