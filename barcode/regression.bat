@echo off

read.py 12345678
read.py 12345-EC-678

read.py 00345678
read.py 02345678
read.py 1234567X
read.py 12345-PAC678
read.py 1234X-EC-678
read.py 12345-EC-67X
read.py 123

echo.
echo Done.
pause
