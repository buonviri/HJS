#!/bin/bash

sudo echo Running antonio22.sh setup

sudo apt install build-essential linux-headers-$(uname -r) gcc-12 libgoogle-glog0v5 -y
sudo add-apt-repository ppa:ubuntu-toolchain-r/test && sudo apt update && sudo apt-get install --only-upgrade libstdc++6 -y
sudo ldconfig

printf "\n\nAdditional instructions:\n\n"
printf "Copy tar file to Home folder and remove any letter suffix, e.g. 2_2_0b -> 2_2_0\n"
printf "Copy and paste the following lines in Terminal and hit enter. Delete tar file upon completion.\n"
printf "cd && tar xvzf dna2_self_test_2_2_0.tar.gz && cd dna2_self_test_2_2_0\n"
printf "chmod +x ./setup_3pg.sh && ./setup_3pg.sh\n"
printf "chmod +x ./run_3pg.sh && ./run_3pg.sh\n"

# EOF
