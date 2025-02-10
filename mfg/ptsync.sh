#!/bin/bash

# too many things can't handle this:
# set -euo pipefail
# IFS=$'\n\t'
# user has to pay attention to outcome!

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n" "$host"

printf "\n\e[1;35m%b\e[0m\n" "Move to prodtest:"
cd ~/prodtest
echo Status $?

printf "\n\e[1;35m%b\e[0m\n" "Update from github:"
git pull
echo Status $?

printf "\n\e[1;35m%b\e[0m\n" "Add new files:"
git add .
echo Status $?

printf "\n\e[1;35m%b\e[0m\n" "Commit:"
git commit -m "$host"
echo Status $?

printf "\n\e[1;35m%b\e[0m\n" "Push to github:"
git push
echo Status $?

echo
# EOF
