@echo off

python.exe S2LP-srread.a.0x10100-void.py
echo .................1
python.exe S2LP-srwrite.a.0x10100.0-void.py
echo .................0
python.exe S2LP-srread.a.0x10100-void.py
echo .................0

python.exe S2LP-pin.AEN_PG1.set-void.py
echo Pin P203..........
python.exe S2LP-srread.a.0x1001C-void.py
echo .................7

python.exe S2LP-srwrite.a.0x1001C.4-void.py
echo .................4
python.exe S2LP-srread.a.0x1001C-void.py
echo .................4

python.exe S2LP-pin.AEN_PG2.set-void.py
echo Pin P310..........
python.exe S2LP-srread.a.0x1001C-void.py
echo .................4

python.exe S2LP-srwrite.a.0x1001C.0-void.py
echo .................0
python.exe S2LP-srread.a.0x1001C-void.py
echo .................0

python.exe S2LP-srwrite.a.0x10100.1-void.py
echo .................1
python.exe S2LP-srread.a.0x10100-void.py
echo .................1

python.exe S2LP-stats-void.py
