#!/bin/bash

echo
echo "A:" | tee 'CB.log'
python3 statlog.py S2LP-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void | tee -a 'CB.log'
echo "(01 00 00)"
python3 statlog.py S2LP-pin.AEN_PG1.set+srread.a.0x1001C-void | tee -a 'CB.log'
echo "(P203 07)"
python3 statlog.py S2LP-srwrite.a.0x1001C.4+srread.a.0x1001C-void | tee -a 'CB.log'
echo "(04 04)"
python3 statlog.py S2LP-pin.AEN_PG2.set+srread.a.0x1001C-void | tee -a 'CB.log'
echo "(P310 04)"
python3 statlog.py S2LP-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void | tee -a 'CB.log'
echo "(00 00 01 01)"

echo
echo "B:" | tee -a 'CB.log'
python3 statlog.py S2LP-srread.b.0x10100+srwrite.b.0x10100.0+srread.b.0x10100-void | tee -a 'CB.log'
echo "(01 00 00)"
python3 statlog.py S2LP-pin.BEN_PG1.set+srread.b.0x1001C-void | tee -a 'CB.log'
echo "(P009 07)"
python3 statlog.py S2LP-srwrite.b.0x1001C.4+srread.b.0x1001C-void | tee -a 'CB.log'
echo "(04 04)"
python3 statlog.py S2LP-pin.BEN_PG2.set+srread.b.0x1001C-void | tee -a 'CB.log'
echo "(P505 04)"
python3 statlog.py S2LP-srwrite.b.0x1001C.0+srread.b.0x1001C+srwrite.b.0x10100.1+srread.b.0x10100-void | tee -a 'CB.log'
echo "(00 00 01 01)"

echo
python3 statlog.py S2LP-stats-void | tee -a 'CB.log'

# EOF
