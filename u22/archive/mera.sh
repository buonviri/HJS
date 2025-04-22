#!/bin/bash

# COMMAND LINE FOR TESTING THIS SCRIPT: cd ~/HJS/u22 && source mera.sh

cd ~/S1LP/install_mera/
source start.sh
cd "$OLDPWD"
mera --version
mera --sakura1_start

# COMMAND LINE TO EXIT = deactivate

# EOF
