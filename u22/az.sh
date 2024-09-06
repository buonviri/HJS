#!/bin/bash

# exit on error
set -e

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

# EOF
