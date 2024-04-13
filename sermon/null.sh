#!/bin/bash

# start a new window that creates a null modem
gnome-terminal -- sh -c 'socat -d -d pty,raw,echo=0,link="/home/ec/COM5" pty,raw,echo=0,link="/home/ec/COM6"'

# EOF
