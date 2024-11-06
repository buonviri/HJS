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

# i: added auto
sudo sensors-detect --auto

# j (x600)
#printf '\nlm92\nnct6775\n# added by EdgeCortix\n\n' | sudo tee -a /etc/modules
#printf '\e[1;35mUpdated file:\e[0m\n' && cat /etc/modules

# k (unnecessary)
grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub
printf '\n\e[1;35m   (Existing command line)\e[0m\n\n'

# lmnop
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4 iommu=pt\"/g' /etc/default/grub
sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"acpi_enforce_resources=lax\"/g' /etc/default/grub
printf '\n\e[1;35m   Fan sensor fix implemented.\e[0m\n\n'
grep GRUB_CMDLINE_LINUX /etc/default/grub
printf '\n\e[1;35m   Confirm pages, iommu, and lax.\e[0m\n\n'
sudo update-grub
printf '\n\e[1;35m   Updated GRUB.\e[0m\n\n'
printf '\n\e[1;35m   WARNING: Next alias will reboot the system!\e[0m\n\n'

# EOF
