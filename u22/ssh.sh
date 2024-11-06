#!/bin/bash

echo

sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh
echo Test using Windows: ssh ec@EC-nnnnS

echo

# end

