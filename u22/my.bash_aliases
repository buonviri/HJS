
# ubuntu aliases by HJS
alias a="sudo apt install git socat xsel -y"
alias b="git clone https://github.com/buonviri/HJS.git"
alias c="cd ~/HJS/u22 && source gnome.sh"
alias d="sudo adduser ec dialout"
alias e="sudo apt install python3-pip -y"
alias f="pip install pyserial"
alias g="pip install pyperclip"
alias h="sudo apt install lm-sensors -y"
alias i="sudo sensors-detect"
alias j="/etc/init.d/kmod start"
alias k="grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub"
alias l="sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4\"/g' /etc/default/grub"
alias m="sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"acpi_enforce_resources=lax\"/g' /etc/default/grub"
alias n="grep GRUB_CMDLINE_LINUX /etc/default/grub"
alias o="sudo update-grub"
alias p="reboot"
alias q="grep HugePages_ /proc/meminfo"
alias r="sensors"
alias s="sudo apt install psensor -y"
alias t="sudo lspci"
alias u="sudo lspci -vvv -s 01:00.0 | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'"
alias v="sudo apt update && sudo apt upgrade"
alias w="sudo apt autoremove"
alias x="sudo apt-get --with-new-pkgs upgrade update-manager"
alias y="sudo apt update && sudo apt upgrade"
alias z="cd ~/HJS/statlog && python3 statlog.py"
alias uu="sudo apt update && sudo apt upgrade"
alias 0="\rm -f ~/.bash_aliases && echo Aliases removed..."
# EOF
