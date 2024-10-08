#!/bin/bash

let "n = 0"  # track current step number

function purple () {
  printf "\e[1;35m%b\e[0m" "$1"
}

function red () {
  printf "\e[1;31m%b\e[0m" "$1"
}

function green () {
  printf "\e[1;32m%b\e[0m" "$1"
}

function check_code () {
  printf "\n  \e[1;35m#%02d:\e[0m %s\n" "$2" "$3"
  if [ $1 -eq 0 ]; then
    green "  Success [$1]\n\n"
  else
    red "  Failed [$1]\n\n"
  fi
}

# always start in Home, DEBUG TODO
# cd

purple "\nStarting setup...\n\n"

# each step must have an id with NO SPACES

id="apt-bad"
((n++))
sudo apt install gitxx # git xsel ntpdate -y
myexitcode=$?
check_code $myexitcode $n $id

id="apt-good"
((n++))
sudo apt install git # git xsel ntpdate -y
myexitcode=$?
check_code $myexitcode $n $id


# cd ~/HJS/u22  # temp, return to test dir DEBUG TODO

purple "THE END ($n)\n\n"

# snipppets:

# echo
# read -n 1 -r -p "Hit any key to continue..."
# echo

# EOF

