#!/bin/bash

echo Creating Null Model Loopback...
gnome-terminal -- sh -c 'socat -d -d pty,raw,echo=0,link="/home/ec/NullModemA" pty,raw,echo=0,link="/home/ec/NullModemB"'
sleep 1

echo After server starts, run this command in a new window, added to clipboard using xsel:
echo
echo '   cd ~/S1LP/inference && python3 serial_client.py'
echo 'cd ~/S1LP/inference && python3 serial_client.py' | xsel -ib
echo
cd ~/S1LP/install_mera/ && source start.sh && mera --sakura1_start && cd ~/S1LP/inference && python3 serial_server.py

# echo and clipboard, not part of script
# cd ~/S1LP/inference && python3 serial_client.py

# EOF
