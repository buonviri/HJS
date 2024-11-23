#!/bin/bash

sudo echo Running antonio.sh

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

sudo apt install gcc-12 picocom  # added by HJS

printf "\n\nAdditional instructions:\n\n"
printf "cd ~/S2LP\n"
printf "tar xvzf dna2_self_test.tar.gz\n"
printf "cd dna2_self_test\n"
printf "chmod +x ./setup.sh\n"
printf "./setup.sh\n"
printf "chmod +x ./run.sh\n"
printf "./run.sh\n"

# EOF
