#!/bin/bash

sudo echo Running antonio.sh

sudo apt install build-essential linux-headers-$(uname -r) gcc-12 libgoogle-glog0v5 -y
sudo add-apt-repository ppa:ubuntu-toolchain-r/test && sudo apt update && sudo apt-get install --only-upgrade libstdc++6 -y
sudo ldconfig

printf "\n\nAdditional instructions:\n\n"
printf "Copy tar file to new folder ~/S2LP\n"
printf "cd ~/S2LP && tar xvzf dna2_self_test_2_2_0.tar.gz\n"
printf "cd dna2_self_test_2_2_0\n"
printf "chmod +x ./setup_3pg.sh && ./setup_3pg.sh\n"
printf "chmod +x ./run_3pg.sh && ./run_3pg.sh\n"

# EOF
