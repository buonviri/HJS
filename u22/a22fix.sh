#!/bin/bash

sudo printf "\nRunning a22fix.sh\n\n"  # force root login

cd ~/dna2_self_test_2_2_0/  # change to self test

yes | \cp -v ~/HJS/mfg/setup_3pg.sh .
chmod +x ./setup_3pg.sh
yes | \cp -v ~/HJS/mfg/setup_3pg_none.sh .
chmod +x ./setup_3pg_none.sh
yes | \cp -v ~/HJS/mfg/setup_3pg_one.sh .
chmod +x ./setup_3pg_one.sh
yes | \cp -v ~/HJS/mfg/setup_3pg_zero.sh .
chmod +x ./setup_3pg_zero.sh
yes | \cp -v ~/HJS/mfg/run_3pg.sh .
chmod +x ./run_3pg.sh

# EOF
