#!/bin/bash

echo
echo A:
python3 statlog.py S2LP-srread.a.0x10100-void
echo ................01
python3 statlog.py S2LP-srwrite.a.0x10100.0-void
echo ................00
python3 statlog.py S2LP-srread.a.0x10100-void
echo ................00

python3 statlog.py S2LP-pin.AEN_PG1.set-void
echo Pin P203..........
python3 statlog.py S2LP-srread.a.0x1001C-void
echo ................07

python3 statlog.py S2LP-srwrite.a.0x1001C.4-void
echo ................04
python3 statlog.py S2LP-srread.a.0x1001C-void
echo ................04

python3 statlog.py S2LP-pin.AEN_PG2.set-void
echo Pin P310..........
python3 statlog.py S2LP-srread.a.0x1001C-void
echo ................04

python3 statlog.py S2LP-srwrite.a.0x1001C.0-void
echo ................00
python3 statlog.py S2LP-srread.a.0x1001C-void
echo ................00

python3 statlog.py S2LP-srwrite.a.0x10100.1-void
echo ................01
python3 statlog.py S2LP-srread.a.0x10100-void
echo ................01

echo
echo B:
python3 statlog.py S2LP-srread.b.0x10100-void
echo ................01
python3 statlog.py S2LP-srwrite.b.0x10100.0-void
echo ................00
python3 statlog.py S2LP-srread.b.0x10100-void
echo ................00

python3 statlog.py S2LP-pin.BEN_PG1.set-void
echo Pin P009..........
python3 statlog.py S2LP-srread.b.0x1001C-void
echo ................07

python3 statlog.py S2LP-srwrite.b.0x1001C.4-void
echo ................04
python3 statlog.py S2LP-srread.b.0x1001C-void
echo ................04

python3 statlog.py S2LP-pin.BEN_PG2.set-void
echo Pin P505..........
python3 statlog.py S2LP-srread.b.0x1001C-void
echo ................04

python3 statlog.py S2LP-srwrite.b.0x1001C.0-void
echo ................00
python3 statlog.py S2LP-srread.b.0x1001C-void
echo ................00

python3 statlog.py S2LP-srwrite.b.0x10100.1-void
echo ................01
python3 statlog.py S2LP-srread.b.0x10100-void
echo ................01

echo
python3 statlog.py S2LP-stats-void

# EOF
