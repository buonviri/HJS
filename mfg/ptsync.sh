#!/bin/bash

# too many things can't handle this:
# set -euo pipefail
# IFS=$'\n\t'
# user has to pay attention to outcome!

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n" "$host"

printf "\nNavigate to prodtest:\n"
cd ~/prodtest
foo=$?
if [ $foo -ne 0 ]; then
  echo "   [error code $foo]"
else
  echo "   Done"
fi

printf "\nUpdate from github:\n"
git pull
foo=$?
if [ $foo -ne 0 ]; then
  echo "   [error code $foo]"
else
  echo "   Done"
fi

printf "\nAdd new files:\n" 
git add .
foo=$?
if [ $foo -ne 0 ]; then
  echo "   [error code $foo]"
else
  echo "   Done"
fi

printf "\nCommit:\n"
git commit -m "$host"
foo=$?
if [ $foo -ne 0 ]; then
  echo "   [error code $foo]"
else
  echo "   Done"
fi

printf "\nPush to github:\n"
git push
foo=$?
if [ $foo -ne 0 ]; then
  echo "   [error code $foo]"
else
  echo "   Done"
fi

echo
# EOF
