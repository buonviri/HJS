#!/bin/bash

let "n = 0"  # track current step number
cd  # always start in Home

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

sudo echo  # ensure password has been entered, print blank line
hostname=$(hostname)  # store for use in log
purple "Starting setup on $hostname...\n\n"  # print to terminal
filename=$(printf "%s.info" "$hostname")  # generate filename
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
echo This step is obsolete: Copying statlog.py to create alternate commands.  # echo, since copy script has no output
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
printf "Writing sensor info to ~/.sensors\n" && sudo sensors-detect --auto > ~/.sensors  #  way too much spam, write to file instead
check_code $? $n $id

id="/etc/modules"
((n++))
cd ~/HJS/u22 && source sensors.sh && cd  # add sensor names to /etc/modules
check_code $? $n $id

id="grub-before"
((n++))
echo before:
\grep GRUB_CMDLINE_LINUX_DEFAULT= /etc/default/grub
check_code $? $n $id

id="grub-mod"
((n++))
echo Modifying /etc/default/grub...  # since sed has no output
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4 iommu=pt\"/g' /etc/default/grub
check_code $? $n $id

id="grub-after"
((n++))
echo after:
\grep GRUB_CMDLINE_LINUX_DEFAULT= /etc/default/grub
check_code $? $n $id

id="grub-before"
((n++))
echo before:
\grep GRUB_CMDLINE_LINUX= /etc/default/grub
check_code $? $n $id

id="grub-mod"
((n++))
echo Modifying /etc/default/grub...  # since sed has no output
sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"acpi_enforce_resources=lax\"/g' /etc/default/grub
check_code $? $n $id

id="grub-after"
((n++))
echo after:
\grep GRUB_CMDLINE_LINUX= /etc/default/grub
check_code $? $n $id

id="update-grub"
((n++))
sudo update-grub
check_code $? $n $id

# next script should start with alias r

id="the-end"
cd ~/HJS/u22
purple "The End ($n)\n\n"

echo 'Hit any key to reboot (not yet implemented, try hitting q instead)...'  # TODO fix this

# snippets:

# echo
# read -n 1 -r -p "Hit any key to continue..."
# echo

# EOF

