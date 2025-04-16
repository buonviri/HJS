@echo off

read8.py 12345678
read8.py 12345-EC-678

read8.py 00345678
read8.py 02345678
read8.py 1234567X
read8.py 12345-PAC678
read8.py 1234X-EC-678
read8.py 12345-EC-67X

echo.
echo Done.
pause
