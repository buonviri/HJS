#!/bin/bash

# make sure socat is installed (sudo apt install socat)

# start a new window that creates a null modem, window is otherwise unusable
gnome-terminal -- sh -c 'socat -d -d pty,raw,echo=0,link="/home/ec/COM5" pty,raw,echo=0,link="/home/ec/COM6"'

# start in same terminal, gets spammy
# socat -d -d pty,raw,echo=0,link="/home/ec/COM5" pty,raw,echo=0,link="/home/ec/COM6" &

echo Starting 9128B serial monitor...
cd ~/HJS/sermon
python3 sm-9182.py

# EOF
