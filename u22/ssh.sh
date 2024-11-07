#!/bin/bash

echo

machine=$(hostname)
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh
echo
echo Test using Windows: ssh ec@"$machine"

echo

# end

