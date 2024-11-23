#!/bin/bash

sudo echo running antonio.sh

sudo apt install build-essential linux-headers-$(uname -r) -y
sudo add-apt-repository ppa:ubuntu-toolchain-r/test && sudo apt update && sudo apt-get install --only-upgrade libstdc++6 -y

mkdir libft
cd libft
wget https://ftdichip.com/wp-content/uploads/2022/06/libft4222-linux-1.4.4.170.tgz
tar xvzf libft4222-linux-1.4.4.170.tgz
sudo ./install4222.sh
cd -
rm -rf libft
sudo ldconfig

# EOF
