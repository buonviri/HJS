@echo off

echo Compute Node A:
python.exe statlog.py S2LP-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void
python.exe statlog.py S2LP-pin.AEN_PG1.set+srread.a.0x1001C-void
python.exe statlog.py S2LP-srwrite.a.0x1001C.4+srread.a.0x1001C-void
python.exe statlog.py S2LP-pin.AEN_PG2.set+srread.a.0x1001C-void
python.exe statlog.py S2LP-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void

echo Compute Node B:
python.exe statlog.py S2LP-srread.b.0x10100+srwrite.b.0x10100.0+srread.b.0x10100-void
python.exe statlog.py S2LP-pin.BEN_PG1.set+srread.b.0x1001C-void
python.exe statlog.py S2LP-srwrite.b.0x1001C.4+srread.b.0x1001C-void
python.exe statlog.py S2LP-pin.BEN_PG2.set+srread.b.0x1001C-void
python.exe statlog.py S2LP-srwrite.b.0x1001C.0+srread.b.0x1001C+srwrite.b.0x10100.1+srread.b.0x10100-void

python.exe statlog.py S2LP-stats-void

echo THE END
