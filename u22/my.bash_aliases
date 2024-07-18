
# ubuntu aliases by HJS v1.06
alias a="sudo apt install git xsel ntpdate -y; printf '\nConfirm that installation succeeded.\n\n'"
alias b="git clone https://github.com/buonviri/HJS.git"
alias c="cd ~/HJS/u22 && source ec.sh"
alias d="sudo adduser ec dialout"
alias e="sudo apt install python3-pip -y"
alias f="pip install pyserial; printf '\nIgnore warning about path.\n\n'"
alias g="pip install pyperclip"
alias h="sudo apt install lm-sensors -y"
alias i="sudo sensors-detect"
alias j="printf '\nTo continue, enter the motherboard name: [b660/x300/x600]...\n\n'"
alias k="grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub; printf '\n(Existing command line)\n\n'"
alias l="printf '\nTo continue, enter the CPU manufacturer [amd/intel]...\n\n'"
alias m="sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"acpi_enforce_resources=lax\"/g' /etc/default/grub; printf '\nFan sensor fix implemented.\n\n'"
alias n="grep GRUB_CMDLINE_LINUX /etc/default/grub; printf '\nConfirm pages, iommu, and lax.\n\n'"
alias o="sudo update-grub"
alias p="printf '\nWARNING: Next alias will reboot the system!\n\n'"
alias q="reboot"
alias r="grep HugePages_ /proc/meminfo; printf '\nConfirm 4/4/0/0.\n\n'"
alias s="sensors; printf '\nConfirm fan and temp sensors.\n\n'"
alias t="sudo lspci && printf '\nConfirm 01:00.0\n\n'"
alias u="sudo lspci -vvv -s 01:00.0 | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'  && printf '\nConfirm 8M/8M/8M/8G/x16.\n\n'"
alias v="sudo apt update && sudo apt upgrade"
alias w="printf '\nDowngrade numpy:\npip install --force-reinstall -v numpy==1.26.4\n\n' "


alias z="cd ~/HJS/statlog && python3 statlog.py"
alias uu="sudo apt update && sudo apt upgrade"
alias 0="\rm -f ~/.bash_aliases && echo Aliases removed..."
alias bios="systemctl reboot --firmware-setup"
alias amd="sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4 iommu=pt\"/g' /etc/default/grub"
alias intel="sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4\"/g' /etc/default/grub"
alias b660="printf '\ncoretemp\nnct6775\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias x300="printf '\nnct6775\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias x600="printf '\nlm92\nnct6775\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias u2="sudo lspci -vvv -s 02:00.0 | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'"
alias hjs="cd ~/HJS/u22"
# EOF
