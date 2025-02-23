#!/bin/bash

sudo echo Running antonio22.sh setup

sudo apt install build-essential linux-headers-$(uname -r) gcc-12 libgoogle-glog0v5 -y
sudo add-apt-repository ppa:ubuntu-toolchain-r/test && sudo apt update && sudo apt-get install --only-upgrade libstdc++6 -y
sudo ldconfig

source ~/HJS/u22/a22fix.sh  # fix bugs

# EOF
