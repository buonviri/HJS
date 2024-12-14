#!/bin/bash

sudo echo  # ensure password has been entered, print blank line

machine=$(hostname)
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh
echo

printf "\e[1;35mTest using Windows: ssh ec@%s\n\e[0m" "$machine"

echo

# end

