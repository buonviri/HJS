#!/bin/bash

echo
echo "Compute Node A:" | tee 'CB.log'
python3 statlog.py S2M2-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void | tee -a 'CB.log'
echo " 01 00 00" | tee -a 'CB.log'
python3 statlog.py S2M2-pin.M2EN_PG1.set+srread.a.0x1001C-void | tee -a 'CB.log'
echo " P106 07" | tee -a 'CB.log'
python3 statlog.py S2M2-srwrite.a.0x1001C.4+srread.a.0x1001C-void | tee -a 'CB.log'
echo " 04 04" | tee -a 'CB.log'
python3 statlog.py S2M2-pin.M2EN_PG2.set+srread.a.0x1001C-void | tee -a 'CB.log'
echo " P111 04" | tee -a 'CB.log'
python3 statlog.py S2M2-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void | tee -a 'CB.log'
echo " 00 00 01 01" | tee -a 'CB.log'

echo
python3 statlog.py S2M2-stats-void | tee -a 'CB.log'
echo T >> 'CB.log'
echo H >> 'CB.log'
echo E >> 'CB.log'
echo  >> 'CB.log'
echo E >> 'CB.log'
echo N >> 'CB.log'
echo D >> 'CB.log'

# EOF
