#!/bin/bash

# too many things can't handle this:
# set -euo pipefail
# IFS=$'\n\t'
# user has to pay attention to outcome!

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n" "$host"

printf "\nNavigate to prodtest:\n"
cd ~/prodtest
echo Status $?

printf "\nUpdate from github:\n"
git pull
echo Status $?

printf "\nAdd new files:\n" 
git add .
echo Status $?

printf "\nCommit:\n"
git commit -m "$host"
echo Status $?

printf "\nPush to github:\n"
git push
echo Status $?

echo
# EOF
