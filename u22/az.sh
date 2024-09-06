#!/bin/bash

# exit on error, probably a bad idea
# set -e

# always start in Home
cd

# a
sudo apt install git xsel ntpdate -y
# printf '\n\e[1;35m   Confirm that installation succeeded.\e[0m\n\n'

# b: pull if folder exists, else clone
git -C HJS pull || git clone https://github.com/buonviri/HJS.git
cd ~/HJS/statlog
source alt.sh
cd

# c
cd ~/HJS/u22
source ec.sh

# d
sudo adduser ec dialout

# e f g h
sudo apt install python3-pip -y
pip install pyserial # printf '\n\e[1;35m   Ignore warning about path.\e[0m\n\n'
pip install pyperclip
sudo apt install lm-sensors -y

# EOF
