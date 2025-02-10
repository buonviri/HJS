#!/bin/bash

# too many things can't handle this:
# set -euo pipefail
# IFS=$'\n\t'
# user has to pay attention to outcome!

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n\n" "$host"

cd ~/prodtest
git pull
git add .
git commit -m "$host"
git push

# EOF
