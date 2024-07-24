#!/bin/bash

# compare timestamps
echo Local/NIST/Local time:
date '+%H:%M:%S'
ntpdate -q time.nist.gov | grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
date '+%H:%M:%S'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename: $hexstamp

# start card - now done by typing mera (alias)
# cd ~/S1LP/install_mera/
# source start.sh
# mera --sakura1_start
# cd "$OLDPWD"

# change to test folder, run, return to previous folder
cd ~/S1LP/inference/
python run_models.py --csv_name $hexstamp
cd "$OLDPWD"

# EOF
