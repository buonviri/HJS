@echo off

echo.
echo Compute Node A:
python.exe statlog.py S2M2-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void
echo. 01 00 00
python.exe statlog.py S2M2-pin.M2EN_PG1.set+srread.a.0x1001C-void
echo. P106 07
python.exe statlog.py S2M2-srwrite.a.0x1001C.4+srread.a.0x1001C-void
echo. 04 04 
python.exe statlog.py S2M2-pin.M2EN_PG2.set+srread.a.0x1001C-void
echo. P111 04
python.exe statlog.py S2M2-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void
echo. 00 00 01 01

echo.
python.exe statlog.py S2M2-stats-void

echo.
echo THE END
