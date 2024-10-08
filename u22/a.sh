#!/bin/bash

let "n = 0"  # track current step number
cd # always start in Home

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
  printf "  \e[1;35m#%02d:\e[0m %s\n" "$2" "$3"
  if [ $1 -eq 0 ]; then
    green "  Success [$1]\n\n"
  else
    red "  Failed [$1]\n\n"
  fi
}

# start of script

hostname=$(hostname)  # store for use in log
purple "\nStarting setup on $hostname...\n\n"

# each step must have an id with NO SPACES

id="apt-install"
((n++))
sudo apt install git xsel ntpdate -y  # install new applications
myexitcode=$?
check_code $myexitcode $n $id

id="HJS-repo"
((n++))
git -C HJS pull || git clone https://github.com/buonviri/HJS.git  # first try to pull, on failure clone instead
myexitcode=$?
check_code $myexitcode $n $id

id="alt-statlog"
((n++))
echo Copying statlog.py to create alternate commands.
cd ~/HJS/statlog && source alt.sh && cd  # make copies
myexitcode=$?
check_code $myexitcode $n $id

# add more here

id="the-end"
cd ~/HJS/u22
purple "The End ($n)\n\n"

# snipppets:

# echo
# read -n 1 -r -p "Hit any key to continue..."
# echo

# EOF

