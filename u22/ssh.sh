#!/bin/bash

sudo echo  # ensure password has been entered, print blank line

machine=$(hostname)
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh
echo
echo Test using Windows: ssh ec@"$machine"

echo

# end

