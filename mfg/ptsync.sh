#!/bin/bash

# too many things can't handle this:
# set -euo pipefail
# IFS=$'\n\t'
# user has to pay attention to outcome!

host=$(hostname)  # get hostname
printf "\nStoring prodtest files for: %s\n" "$host"

printf "\nNavigate to prodtest:\n"
cd ~/prodtest  # ------------------------------- cd
foo=$?
if [ $foo -ne 0 ]; then
  printf "   \e[1;31m[ERROR CODE $foo]\e[0m\n"
else
  echo "   Done"
  printf "\nUpdate from github:\n"
  git pull  # ---------------------------------- pull
  foo=$?
  if [ $foo -ne 0 ]; then
    printf "   \e[1;31m[ERROR CODE $foo]\e[0m\n"
  else
    echo "   Done"
    printf "\nAdd new files:\n" 
    git add .  # ------------------------------- add
    foo=$?
    if [ $foo -ne 0 ]; then
      printf "   \e[1;31m[ERROR CODE $foo]\e[0m\n"
    else
      echo "   Done"
      printf "\nCommit:\n"
      git commit -m "$host"
      foo=$?
      if [ $foo -ne 0 ]; then
        printf "   \e[1;31m[ERROR CODE $foo]\e[0m\n"
      else
        echo "   Done"
      fi
      printf "\nPush to github:\n"
      git push
      foo=$?
      if [ $foo -ne 0 ]; then
        printf "   \e[1;31m[ERROR CODE $foo]\e[0m\n"
      else
        echo "   Done"
      fi  # end ?
    fi  # end add
  fi  # end pull
fi  # end cd

echo
# EOF
