
# ubuntu aliases by HJS
alias old_r="grep HugePages_ /proc/meminfo; printf '\n\e[1;35m   Confirm 4/4/0/0.\e[0m\n\n'"
alias old_s="sensors; printf '\e[1;35m   Confirm fan and temp sensors.\e[0m\n\n'"
alias old_t="sudo lspci | grep -i 1fdc:.... || echo Device not found: 1fdc:nnnn;printf '\n\e[1;35m   Confirm xx:00.0 is Co-processor with Device ID 1fdc:nnnn.\e[0m\n\n'"
alias old_u="sudo lspci -vvv -d 1fdc: | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'  | awk '{\$1=\$1;print}' && printf '\n\e[1;35m   Confirm 8M/8M/8M/8GT/x16.\e[0m\n\n'"
alias uu="sudo apt update -y && sudo apt upgrade -y"
alias ar="sudo apt autoremove -y"
alias 00="poweroff"
alias 01="reboot"
alias bios="systemctl reboot --firmware-setup"
alias hjs="cd ~/HJS/u22"
alias mfg="cd ~/HJS/mfg"
alias snap="killall snap-store && snap refresh"
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
alias sysinfo="cd ~/HJS/u22 && source sysinfo.sh"
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
# alias is obsolete (S1LP)
alias pci="source ~/HJS/u22/pcie.sh"
alias pcie="source ~/HJS/u22/pcie.sh"
alias 1fdc="sudo lspci -vvv -d 1fdc: | \\grep -E '1fdc|Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:' | tee ~/pci.info"
alias fans="sensors | grep fan | grep -v ':[ \\t]\\+0 RPM' || echo No fans detected."
alias dimms="sudo dmidecode -t memory | grep -E 'Manufacturer:|Serial Number:|Part Number:|Volatile Size:.+GB' | grep -v -E 'Unknown|Not Specified' | awk '{\$1=\$1;print}' | tee ~/mem.info"
alias temps="sensors | \grep ':.*+.*C'"
alias aspm="source ~/HJS/u22/aspm.sh"
alias lab="echo && sudo echo 'Running us-we-ptsync-uu' && echo ; us ; we ; ptsync ; uu ; cd"
alias lab-="echo && echo 'Running us-we-ptsync' && echo ; us ; we ; ptsync ; cd"
alias us="cd ~/HJS/u22 && git pull && source ./us.sh"
alias we="cd ~/hex-ftdi-cfg && git pull"
alias us2them="cd ~/HJS/u22 && git pull && source ./them.sh"
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
alias usb="python3 ~/HJS/u22/lsusb.py | tee ~/usb.info"
alias usbsn="lsusb -v -d 0403: 2> /dev/null > ~/ftdi.info && cat ~/ftdi.info | \\grep -E 'idVendor|idProduct|iManufacturer|iProduct|iSerial'"
alias imdt="screen /dev/ttyUSB0 115200"
alias jam="source ~/HJS/u22/jam.sh"
alias mem="free -m"
alias catinfo="tail -n +1 ~/*.info"
alias epoch="source ~/HJS/u22/epoch.sh"
alias e2="printf '\nsudo -i\n~/.local/share/renesas/e2_studio/eclipse/e2studio&\n\n'"
alias avatar="pactl get-sink-volume @DEFAULT_SINK@ | grep Volume ; eog /var/lib/AccountsService/icons/ec"
alias catme="cat ~/EC*.info"
alias m22="s2res ; cd ~/mera_package/install_mera && source install_all_steps.sh && mera --version"
alias a22="source ~/HJS/u22/a22.sh"
# Start of S2 utils
alias maxfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.100+fan-void"
alias minfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.40+fan-void"
alias s2="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'stats' | picocom -qrix 100 /dev/ttyUSB0"
alias stats="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'stats' | picocom -qrix 100 /dev/ttyUSB0"
alias statslog="cd && python3 ~/HJS/statlog/statlog.py S2XX-statslog"
alias cb12="cd ~/HJS/statlog && source ./CB12.sh"
alias cb00="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+0+0+[]+[]+[]+[]+[]+[]+C-fast"
alias cb20="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+2+0+[]+[]+[]+[]+[]+[]+C-fast"
alias cb22="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+2+2+[]+[]+[]+[]+[]+[]+C-fast"
alias stayon+="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.bist.stayon+C-fast"
alias stayon-="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.bist.[DASH]stayon+C-fast"
alias bmc="info | tee ~/bmc.info && printf '\nBoth should be 0x18 on dual cards\n' && c008c | tee -a ~/bmc.info"
alias qbmc="~/mera_package/bmc GetBmcInfor"
# alias is obsolete
alias xl2="source ~/hex-ftdi-cfg/hex/xl2.sh ; pt ; printf '\nCycle Power...\n\n'"
# alias is obsolete
alias a440="aplay /home/ec/HJS/u22/wav/440.wav --quiet"
alias fault="source ~/HJS/u22/faultcodes.sh"
alias info="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'info' | picocom -qrix 100 /dev/ttyUSB0"
alias c008c="python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C-void"
alias c008c-dual="python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void"
alias xlog="xlogver | tee ~/zog.info && xlogslow | tee -a ~/zog.info"
alias qxlog="~/mera_package/bmc RetrieveXlogData"
alias xlogver="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'ver' | picocom -qrix 100 /dev/ttyUSB0"
alias xlogslow="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'xlog' | picocom -qrix 500 /dev/ttyUSB0"
alias xxlog="python3 ~/HJS/statlog/statlog.py S2XX-ver-null | tee ~/zog.info && python3 ~/HJS/statlog/statlog.py S2XX-xlog-wait | tee -a ~/zog.info"
alias xerr="cat ~/zog.info | grep -i -E 'pass|fail|errors|error|fault'"
alias xerrf="cat ~/zog.info | grep -i -E 'fail|errors|error|fault' || printf '\e[1;31mNone\e[0m\n'"
alias xx="xlog && echo 'Pass | Fail | Error | Fault' && xerr"
alias xxf="xlog && echo 'Fail | Error | Fault' && xerrf"
alias xxx="xxlog && echo 'Pass | Fail | Error | Fault' && xerr"
alias cfg="cfga && cfgb"
alias cfga="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'ver' | picocom -qrix 100 /dev/ttyUSB0 | tee ~/cfg.info"
alias cfgb="picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0 && echo 'cfg' | picocom -qrix 100 /dev/ttyUSB0 | tee -a ~/cfg.info"
alias cfg4pt="python3 ~/HJS/mfg/cfg4pt.py"
alias enpg="python3 ~/HJS/statlog/statlog.py S2LP-pins.[QUOTE][STAR]EN_PG[STAR][QUOTE]-void"
alias s2do="python3 ~/HJS/statlog/statlog.py S2XX"
alias s2i="source ~/HJS/u22/S2xx.sh"
alias s2icb="source ~/HJS/u22/S2xx-cb.sh"
alias s2s="mera --lssakura | tee ~/sak.info"
alias qok="~/mera_package/bmc BoardStatusCmd"
alias s2env="source ~/HJS/u22/S2env.sh"
alias de="deactivate"
# End of S2 utils, start of S2 models
alias models="printf '\n\e[1;35m   detr effnet resnet\n   hf1 hf2 hf3 hf4\n   yolov5 yolov7 yolov8\e[0m\n\n'"
alias detr="source ~/HJS/u22/model.sh detr"
alias effnet="source ~/HJS/u22/model.sh efficient_net_demo"
alias resnet="source ~/HJS/u22/model.sh resnet50"
alias hf1="source ~/HJS/u22/model.sh huggingface_image_classification"
alias hf2="source ~/HJS/u22/model.sh huggingface_image_segmentation"
alias hf3="source ~/HJS/u22/model.sh huggingface_text_classification"
alias hf4="source ~/HJS/u22/model.sh huggingface_text_gen"
alias yolov5="source ~/HJS/u22/model.sh yolov5"
alias yolov7="source ~/HJS/u22/model.sh yolov7"
alias yolov8="source ~/HJS/u22/model.sh yolov8"
alias ten="s2clr ; s2i && detr && effnet && resnet && hf1 && hf2 && hf3 && hf4 && yolov5 && yolov7 && yolov8 && cd ; de"
alias res="eog result*.png"
alias s2clr="source ~/HJS/u22/mera22clr.sh"
alias s2res="\cp -v ~/HJS/u22/results-mera22.html ~/mera_package/examples/results.html ; \cp -v ~/HJS/u22/img/eci.svg ~/mera_package/examples/eci.svg; \cp -v ~/HJS/mfg/setup_none.sh ~/mera_package/initialize_sakura_ii/setup_none.sh"
alias prodtest="source ~/prodtest/bin/prodtest.sh"
alias pt="source ~/prodtest/bin/prodtest.sh"
alias pt+="echo 'enabling auto-prodtest' ; echo 'The world is a vampire' > ~/.auto_prodtest"
alias pt-="printf 'disabling auto-prodtest: ' ; rm -v ~/.auto_prodtest 2>&1 | \grep removed || echo 'already disabled'"
# alias is obsolete
alias ptsync="source ~/prodtest/bin/ptsync.sh"
alias bist="source ~/prodtest/bin/bist.sh"
# alias is obsolete
alias b8="printf '\n\e[1;35mRun xxf to summarize failures...\e[0m\n' && bist 8"
alias sn="source ~/prodtest/bin/sn.sh"
alias last="source ~/.last_sn"
alias ptas="prodtest && printf '\e[1;35m->\e[0m\n' && ptsync"
alias lot="source ~/prodtest/bin/lot.sh"
alias lots="python3 ~/prodtest/bin/lots.py"
alias telem="cd ~/mera_package/telemetry_sakura_ii && ./telemetry 0 1 50 > ~/telem.info && cd && python3 ~/HJS/u22/telem.py"
alias ant22="printf 'This alias is obsolete. Use dryi (dry init) instead.\n'"
alias dryi="sudo echo 'dry init with dma_test:' && cd ~/dna2_self_test_2_2_0/ && ./setup_3pg_zero.sh ; echo ; printf '\e[1;35m   Ensure that compute blocks 01 and 02 are enabled.\e[0m\n\n'"
alias drybi="sudo echo 'dry init with dma_test:' && cd ~/dna2_self_test_2_2_0/ && ./setup_3pg_one.sh ; echo ; printf '\e[1;35m   Ensure that compute blocks 01 and 02 are enabled.\e[0m\n\n'"
alias d00="~/dna2_self_test_2_2_0/dma_test 0 ddr0 1048576"
alias d01="~/dna2_self_test_2_2_0/dma_test 0 ddr1 1048576"
alias d10="~/dna2_self_test_2_2_0/dma_test 1 ddr0 1048576"
alias d11="~/dna2_self_test_2_2_0/dma_test 1 ddr1 1048576"
alias dma="source ~/HJS/u22/dma22.sh"
alias dma1k="source ~/HJS/u22/dma1k.sh"
# alias is obsolete
# alias is obsolete
alias dry="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh"
# alias is obsolete
# alias is obsolete
alias dry3="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 999"
alias dry3b="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 999 1"
alias dry4="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 9999"
alias dry5="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 99999"
alias trump="source ~/prodtest/bin/trump.sh"
alias d3="source ~/prodtest/bin/timezero.sh ; dryi ; echo "..." ; dry3 ; source ~/prodtest/bin/time.sh"
alias d3b="source ~/prodtest/bin/timezero.sh ; drybi ; echo "..." ; dry3b ; source ~/prodtest/bin/time.sh"
alias t6="trump 6"
alias 2dot02="cat ~/prodtest/10015/*.txt | \grep -o '10015[0-9][0-9][0-9]+1+5+1066+2\[DOT\]02.*1+98' | sed 's/+/ /g' | sed 's/10015/10015-/g'"
alias 2dot02b="cat ~/prodtest/10000/*.txt | \grep -o '10000[0-9][0-9][0-9]+1+5+1066+2\[DOT\]02.*1+98' | sed 's/+/ /g' | sed 's/10000/10000-/g'"
alias t988585="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+98+85+85+[]+[]+C-fast"
alias t988580="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+98+85+80+[]+[]+C-fast"
# RPI5
alias pi="source ~/HJS/u22/pi.sh"
# Version
alias ver="printf '\n\e[1;35m   HJS aliases v4.13\e[0m\n\n'"
# EOF
