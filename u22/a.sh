#!/bin/bash

function check_code () {
  # printf "\nprintf test: $1\n\n"
  # echo "echo test" $1
  if [ $1 -eq 0 ]; then
    printf "\n\e[1;32mSuccess\e[0m\n\n"
  else
    printf "\n\e[1;31mFailed with code $1\e[0m\n\n"
    # echo Failed with code $1
  fi
}

# always start in Home, DEBUG TODO
# cd

printf "\n\e[1;35mStarting setup...\e[0m\n\n"

# a
sudo apt install gitxx # git xsel ntpdate -y
myexitcode=$?
check_code $myexitcode

# echo
# read -n 1 -r -p "Hit any key to continue..."
# echo

sudo apt install git # git xsel ntpdate -y
myexitcode=$?
check_code $myexitcode


# cd ~/HJS/u22  # temp, return to test dir DEBUG TODO

printf "\e[1;35mTHE END\e[0m\n\n"

# EOF

