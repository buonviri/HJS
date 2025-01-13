#!/bin/bash

# this script assumes the mera tar file has been unzipped and placed in ~/S2xx already

# need this once per system (removed picocom from original version):
sudo apt install build-essential linux-headers-$(uname -r) gcc-12
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update && sudo apt-get install --only-upgrade libstdc++6

# install
cd ~/S2xx/install_mera
./install_os_dependencies.sh
./create_virtual_env.sh && source start.sh
./install_mera_and_python_dependencies.sh
./install_mera_models_and_python_dependencies.sh
./install_mera_visualizer_and_python_dependencies.sh
echo
echo MERA 2.2 setup is complete
echo Deactivating...
deactivate

# EOF
