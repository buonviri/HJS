#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n\n" "$host"

cd ~/prodtest
git pull
git add .
git commit -m "$host"
git push

# EOF
