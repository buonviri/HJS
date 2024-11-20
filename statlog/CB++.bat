@echo off

echo A:
python.exe S2LP-srread.a.0x10100-void.py
echo ................01
python.exe S2LP-srwrite.a.0x10100.0-void.py
echo ................00
python.exe S2LP-srread.a.0x10100-void.py
echo ................00

python.exe S2LP-pin.AEN_PG1.set-void.py
echo Pin P203..........
python.exe S2LP-srread.a.0x1001C-void.py
echo ................07

python.exe S2LP-srwrite.a.0x1001C.4-void.py
echo ................04
python.exe S2LP-srread.a.0x1001C-void.py
echo ................04

python.exe S2LP-pin.AEN_PG2.set-void.py
echo Pin P310..........
python.exe S2LP-srread.a.0x1001C-void.py
echo ................04

python.exe S2LP-srwrite.a.0x1001C.0-void.py
echo ................00
python.exe S2LP-srread.a.0x1001C-void.py
echo ................00

python.exe S2LP-srwrite.a.0x10100.1-void.py
echo ................01
python.exe S2LP-srread.a.0x10100-void.py
echo ................01

echo B:
python.exe S2LP-srread.b.0x10100-void.py
echo ................01
python.exe S2LP-srwrite.b.0x10100.0-void.py
echo ................00
python.exe S2LP-srread.b.0x10100-void.py
echo ................00

python.exe S2LP-pin.BEN_PG1.set-void.py
echo Pin P009..........
python.exe S2LP-srread.b.0x1001C-void.py
echo ................07

python.exe S2LP-srwrite.b.0x1001C.4-void.py
echo ................04
python.exe S2LP-srread.b.0x1001C-void.py
echo ................04

python.exe S2LP-pin.BEN_PG2.set-void.py
echo Pin P505..........
python.exe S2LP-srread.b.0x1001C-void.py
echo ................04

python.exe S2LP-srwrite.b.0x1001C.0-void.py
echo ................00
python.exe S2LP-srread.b.0x1001C-void.py
echo ................00

python.exe S2LP-srwrite.b.0x10100.1-void.py
echo ................01
python.exe S2LP-srread.b.0x10100-void.py
echo ................01

python.exe S2LP-stats-void.py
