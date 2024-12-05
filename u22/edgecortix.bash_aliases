
# ubuntu aliases by HJS
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
alias r="grep HugePages_ /proc/meminfo; printf '\n\e[1;35m   Confirm 4/4/0/0.\e[0m\n\n'"
alias s="sensors; printf '\e[1;35m   Confirm fan and temp sensors.\e[0m\n\n'"
alias t="sudo lspci | grep -i 1fdc:.... || echo Device not found: 1fdc:nnnn;printf '\n\e[1;35m   Confirm xx:00.0 is Co-processor with Device ID 1fdc:0100.\e[0m\n\n'"
alias u="sudo lspci -vvv -d 1fdc:0100 | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'  | awk '{\$1=\$1;print}' && printf '\n\e[1;35m   Confirm 8M/8M/8M/8GT/x16.\e[0m\n\n'"
alias v="sudo apt update && sudo apt upgrade"
alias w="printf '\n\e[1;35m   Downgrade numpy:\n   pip install --force-reinstall -v numpy==1.26.4\e[0m\n\n'"
alias x="printf '\n\e[1;35m   The End\e[0m\n\n'"
alias y="printf '\n\e[1;35m   mera-setup camera-setup ips-setup\n   mera16 numpy deploy\e[0m\n\n'"
alias z="printf '\n\e[1;35m   sysinfo mera16 camera\n   fym mde yod\n   meas measu measur measure\n   sjlog ips perf\e[0m\n\n'"
alias uu="sudo apt update && sudo apt upgrade"
alias ar="sudo apt autoremove -y"
alias 00="poweroff"
alias bios="systemctl reboot --firmware-setup"
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
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
alias pcie="source ~/HJS/u22/pcie.sh"
alias 1fdc="sudo lspci -vvv -d 1fdc: | \\grep -E '1fdc|Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:' | tee ~/pci.info"
alias fans="sensors | grep fan | grep -v ':[ \\t]\\+0 RPM' || echo No fans detected."
alias temps="sensors | \grep ':.*+.*C'"
alias aspm="source ~/HJS/u22/aspm.sh"
alias us="cd ~/HJS/u22 && git pull && source ./us.sh"
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
alias usb="python3 ~/HJS/u22/lsusb.py | tee ~/usb.info"
alias imdt="screen /dev/ttyUSB0 115200"
alias jam="source ~/HJS/u22/jam.sh"
# S2
alias maxfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.100+fan-void"
alias minfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.40+fan-void"
alias s2="python3 ~/HJS/statlog/statlog.py S2XX-stats-void"
alias cb12="cd ~/HJS/statlog && source ./CB12.sh"
alias cbm2="cd ~/HJS/statlog && source ./CBM2.sh"
alias bmc="python3 ~/HJS/statlog/statlog.py S2XX-info-void && printf '\nBoth should be 0x18\n' && python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void"
alias info="python3 ~/HJS/statlog/statlog.py S2XX-info-void"
alias xlog="python3 ~/HJS/statlog/statlog.py S2XX-ver-null | tee ~/zog.info && python3 ~/HJS/statlog/statlog.py S2XX-xlog-slow | tee -a ~/zog.info"
alias cfg="python3 ~/HJS/statlog/statlog.py S2XX-ver-null | tee ~/cfg.info && python3 ~/HJS/statlog/statlog.py S2XX-cfg-null | tee -a ~/cfg.info"
# End of S2

alias ver="printf '\n\e[1;35m   HJS aliases v3.02\e[0m\n\n'"
# EOF
