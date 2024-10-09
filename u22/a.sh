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
    printf "[Success] #%02d: %s\n" "$2" "$3" >> $filename
  else
    red "  Failure [$1]\n\n"
    printf "[Failure] #%02d: %s\n" "$2" "$3" >> $filename
  fi
}

# start of script, get hostname and file name

hostname=$(hostname)  # store for use in log
purple "\nStarting setup on $hostname...\n\n"  # print to terminal
filename=$(printf "%s.log" "$hostname")  # generate filename
printf "\n%s: %s\n" "$(date)" "$hostname" >> $filename  # append file with timestamp

# each step must have an id with NO SPACES

id="apt-install"
((n++))
sudo apt install git xsel ntpdate python3-pip lm-sensors -y  # install new applications
check_code $? $n $id

id="pip-install"
((n++))
echo This will fail on systems that disallow pip.
pip install pyserial pyperclip
check_code $? $n $id

id="HJS-repo"
((n++))
git -C HJS pull || git clone https://github.com/buonviri/HJS.git  # first try to pull, on failure clone instead
check_code $? $n $id

id="alt-statlog"
((n++))
echo Copying statlog.py to create alternate commands.  # since copy script has no output
cd ~/HJS/statlog && source alt.sh && cd  # make copies
check_code $? $n $id

id="gnome"
((n++))
cd ~/HJS/u22 && source ec.sh && cd  # gnome settings
check_code $? $n $id

id="dialout"
((n++))
sudo adduser ec dialout  # add user to dialout group for UART access
check_code $? $n $id

id="sensors-detect"
((n++))
sudo sensors-detect --auto
check_code $? $n $id

echo TODO: MOTHERBOARD INFO

id="grub"
((n++))
echo GRUB:
grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub
check_code $? $n $id

id="the-end"
cd ~/HJS/u22
purple "The End ($n)\n\n"

# snipppets:

# echo
# read -n 1 -r -p "Hit any key to continue..."
# echo

# EOF

