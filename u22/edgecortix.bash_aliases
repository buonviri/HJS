
# ubuntu aliases by HJS
alias a="sudo apt install git xsel ntpdate -y; printf '\n\e[1;35m   Confirm that installation succeeded.\e[0m\n\n'"
alias b="git clone https://github.com/buonviri/HJS.git && cd ~/HJS/statlog && source alt.sh && cd"
alias c="cd ~/HJS/u22 && source ec.sh"
alias d="sudo adduser ec dialout"
alias e="sudo apt install python3-pip -y"
alias f="pip install pyserial; printf '\n\e[1;35m   Ignore warning about path.\e[0m\n\n'"
alias g="pip install pyperclip"
alias h="sudo apt install lm-sensors -y"
alias i="printf '\n\e[1;35m   Accept defaults if needed.\e[0m\n\n'; sleep 1; sudo sensors-detect --auto"
alias j="printf '\n\e[1;35m   To continue, enter the motherboard name: [b660/x300/x600/rplp/k803/none]...\e[0m\n\n'"
alias k="grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub; printf '\n\e[1;35m   (Existing command line)\e[0m\n\n'"
alias l="sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"/GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash pcie_aspm=off default_hugepagesz=1G hugepagesz=1G hugepages=4 iommu=pt\"/g' /etc/default/grub"
alias m="sudo sed -i 's/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"acpi_enforce_resources=lax\"/g' /etc/default/grub; printf '\n\e[1;35m   Fan sensor fix implemented.\e[0m\n\n'"
alias n="grep GRUB_CMDLINE_LINUX /etc/default/grub; printf '\n\e[1;35m   Confirm pages, iommu, and lax.\e[0m\n\n'"
alias o="sudo update-grub; printf '\n\e[1;35m   Updated GRUB.\e[0m\n\n'"
alias p="printf '\n\e[1;35m   WARNING: Next alias will reboot the system!\e[0m\n\n'"
alias q="reboot"
alias r="grep HugePages_ /proc/meminfo; printf '\n\e[1;35m   Confirm 4/4/0/0.\e[0m\n\n'"
alias s="sensors; printf '\e[1;35m   Confirm fan and temp sensors.\e[0m\n\n'"
alias t="sudo lspci && printf '\n\e[1;35m   Confirm 01:00.0 is Co-processor with Device ID 1fdc:0100.\e[0m\n\n'"
alias u="sudo lspci -vvv -s 01:00.0 | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'  && printf '\n\e[1;35m   Confirm 8M/8M/8M/8GT/x16.\e[0m\n\n'"
alias v="sudo apt update && sudo apt upgrade"
alias w="printf '\n\e[1;35m   Downgrade numpy:\n   pip install --force-reinstall -v numpy==1.26.4\e[0m\n\n'"
alias x="printf '\n\e[1;35m   The End\e[0m\n\n'"
alias y="printf '\n\e[1;35m   mera-setup camera-setup ips-setup\n   mera16 numpy deploy\e[0m\n\n'"
alias z="printf '\n\e[1;35m   sysinfo mera16 camera\n   fym mde yod\n   meas measu measur measure\n   sjlog ips perf\e[0m\n\n'"
alias uu="sudo apt update && sudo apt upgrade"
alias 00="poweroff"
alias bios="systemctl reboot --firmware-setup"
alias b660="printf '\ncoretemp\nnct6775\n\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias x300="printf '\nnct6775\n# added by EdgeCortix\n\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias x600="printf '\nlm92\nnct6775\n# added by EdgeCortix\n\n' | sudo tee -a /etc/modules && printf '\e[1;35mUpdated file:\e[0m\n' && cat /etc/modules"
alias rplp="printf '\ncoretemp\nnct6775\n\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias k803="printf '\n\e[1;35m   OnLogic K803 is not currently supported - sensor investigation is required.\e[0m\n\n'"
alias fl3="printf '\ncoretemp\n\n# added by EdgeCortix\n' | sudo tee -a /etc/modules && cat /etc/modules"
alias none="printf '\n\e[1;35m   No motherboard chosen.\e[0m\n\n'"
alias hjs="cd ~/HJS/u22"
alias snap="killall snap-store && snap refresh"
alias mera16="cd ~/S1LP/install_mera/ && source start.sh && mera --version && mera --sakura1_start"
alias camera="cd ~/S1LP/camera && ./RUN_DEMO2_FUSED.sh"
alias sysinfo="cd ~/HJS/u22 && source info.sh"
alias camera-setup="cd ~/Downloads/ && cp -v /media/ec/EC/camera/*.tar.gz . && tar xvzf fused_demo_sakura_novenv.tar.gz && mv fused_demo_sakura_novenv ~/S1LP/camera"
alias mera-setup="cd ~/Downloads/ && cp -v /media/ec/EC/mera-1.6/*.tar.gz . && tar xvzf sakura-demo.tar.gz && cd sakura_demo && mv * ~/S1LP/ && cd ~/S1LP/install_mera/ && source install.sh && deactivate"
alias numpy="pip install --force-reinstall -v numpy==1.26.4"
alias deploy="cd ~/S1LP/latency_power_measurement/ && python download.py && python deploy.py --models models/"
alias fym="cd ~/S1LP/demos/fused_yolov5m_monodepth/ && python deploy.py && python demo_model.py && eog *.png"
alias mde="cd ~/S1LP/demos/monodepth_depth_estimation_demo/ && python deploy.py && python demo_model.py && eog *.png"
alias yod="cd ~/S1LP/demos/yolov5_object_detection_demo/ && python deploy.py && python demo_model.py && eog *.png"
alias ips="source ~/S1LP/inference/ips.sh"
alias ips-setup="cd ~/S1LP && cp -v -r /media/ec/EC/hw-benchmarking/inference/ . && cd inference && cp -v -r /media/ec/EC/deployments/ . && mkdir log && python3 sjscan.py"
alias sjlog="cd ~/S1LP/inference/ && python3 sjlog.py"
alias meas="cd ~/S1LP/latency_power_measurement/ && python measure.py --model_path deployments/"
alias measu="cd ~/S1LP/latency_power_measurement/ && MERA_MEASURE_POWER=3 python measure.py --model_path deployments/ --power"
alias measur="cd ~/S1LP/latency_power_measurement/ && python measure.py --model_path precompiled/ --name precompiled"
alias measure="cd ~/S1LP/latency_power_measurement/ && MERA_MEASURE_POWER=3 python measure.py --model_path precompiled/ --name precompiled --power"
alias perf="source ~/S1LP/inference/perf.sh"
alias ver="printf '\n\e[1;35m   HJS aliases v2.54\e[0m\n\n'"
# EOF
