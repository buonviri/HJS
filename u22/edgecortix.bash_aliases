
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
alias t="sudo lspci | grep -i 1fdc:.... || echo Device not found: 1fdc:nnnn;printf '\n\e[1;35m   Confirm xx:00.0 is Co-processor with Device ID 1fdc:nnnn.\e[0m\n\n'"
alias u="sudo lspci -vvv -d 1fdc: | grep -E 'Subsystem:|LnkSta:|Region 0:|Region 2:|Region 4:'  | awk '{\$1=\$1;print}' && printf '\n\e[1;35m   Confirm 8M/8M/8M/8GT/x16.\e[0m\n\n'"
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
alias uu="sudo apt update -y && sudo apt upgrade -y"
alias ar="sudo apt autoremove -y"
alias 00="poweroff"
alias 01="reboot"
alias bios="systemctl reboot --firmware-setup"
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
# alias is obsolete
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
# alias is obsolete
alias fans="sensors | grep fan | grep -v ':[ \\t]\\+0 RPM' || echo No fans detected."
alias dimms="sudo dmidecode -t memory | grep -E 'Manufacturer:|Serial Number:|Part Number:|Volatile Size:.+GB' | grep -v -E 'Unknown|Not Specified' | awk '{\$1=\$1;print}' | tee ~/mem.info"
alias temps="sensors | \grep ':.*+.*C'"
alias aspm="source ~/HJS/u22/aspm.sh"
alias lab="us ; we ; ptsync"
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
alias m22="s2res ; cd ~/mera_package/install_mera && source install_all_steps.sh"
alias a22="source ~/HJS/u22/a22.sh"
# Start of S2 utils
alias maxfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.100+fan-void"
alias minfan="python3 ~/HJS/statlog/statlog.py S2LP-fan.a.40+fan-void"
alias s2="python3 ~/HJS/statlog/statlog.py S2XX-stats-void"
alias stats="python3 ~/HJS/statlog/statlog.py S2XX-stats-void"
alias statslog="cd && python3 ~/HJS/statlog/statlog.py S2XX-statslog"
alias cb12="cd ~/HJS/statlog && source ./CB12.sh"
alias cb00="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.edit+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+[]+0+0+[]+[]+[]+[]+[]+[]+C-fast"
alias stayon+="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.bist.stayon+C-fast"
alias stayon-="python3 ~/HJS/statlog/statlog.py S2XX-cfg.[DASH]unlock+cfg.bist.[DASH]stayon+C-fast"
alias bmc="info | tee ~/bmc.info && printf '\nBoth should be 0x18 on dual cards\n' && c008c | tee -a ~/bmc.info"
alias qbmc="~/mera_package/bmc GetBmcInfor"
alias xl1="source ~/HJS/u22/xl1.sh"
alias xl2="source ~/HJS/u22/xl2.sh"
alias xl3="source ~/HJS/u22/xl3.sh"
alias a440="aplay /home/ec/HJS/u22/wav/440.wav --quiet"
alias fault="source ~/HJS/u22/faultcodes.sh"
alias info="python3 ~/HJS/statlog/statlog.py S2XX-info-void"
alias c008c="python3 ~/HJS/statlog/statlog.py S2LP-srread.a.0xC008C+srread.b.0xC008C-void"
alias xlog="xlogver | tee ~/zog.info && xlogslow | tee -a ~/zog.info"
alias qxlog="~/mera_package/bmc RetrieveXlogData"
alias xlogver="python3 ~/HJS/statlog/statlog.py S2XX-ver-null"
alias xlogslow="python3 ~/HJS/statlog/statlog.py S2XX-xlog-slow"
alias xxlog="python3 ~/HJS/statlog/statlog.py S2XX-ver-null | tee ~/zog.info && python3 ~/HJS/statlog/statlog.py S2XX-xlog-wait | tee -a ~/zog.info"
alias xerr="cat ~/zog.info | grep -i -E 'pass|fail|errors|error|fault'"
alias xerrf="cat ~/zog.info | grep -i -E 'fail|errors|error|fault' || printf '\e[1;31mNone\e[0m\n'"
alias xx="xlog && echo 'Pass | Fail | Error | Fault' && xerr"
alias xxf="xlog && echo 'Fail | Error | Fault' && xerrf"
alias xxx="xxlog && echo 'Pass | Fail | Error | Fault' && xerr"
alias cfg="cfga && cfgb"
alias cfga="python3 ~/HJS/statlog/statlog.py S2XX-ver-null | tee ~/cfg.info"
alias cfgb="python3 ~/HJS/statlog/statlog.py S2XX-cfg-null | tee -a ~/cfg.info"
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
alias prodtest="source ~/HJS/mfg/prodtest.sh"
alias pt="source ~/HJS/mfg/prodtest.sh"
alias pt+="echo 'enabling auto-prodtest' ; echo 'The world is a vampire' > ~/.auto_prodtest"
alias pt-="printf 'disabling auto-prodtest: ' ; rm -v ~/.auto_prodtest 2>&1 | \grep removed || echo 'already disabled'"
alias prodtestn="source ~/HJS/mfg/prodtestn.sh"
alias ptsync="source ~/HJS/mfg/ptsync.sh"
alias bist="source ~/HJS/mfg/bist.sh"
# alias is obsolete
alias b8="printf '\n\e[1;31mRun xxf to summarize failures...\e[0m\n' && bist 8"
alias sn="source ~/HJS/mfg/sn.sh"
alias ptas="prodtest && printf '\e[1;35m->\e[0m\n' && ptsync"
alias lot="source ~/HJS/mfg/lot.sh"
alias lots="python3 ~/HJS/mfg/lots.py"
alias telem="cd ~/mera_package/telemetry_sakura_ii && ./telemetry 0 1 50 > ~/telem.info && cd && python3 ~/HJS/u22/telem.py"
alias ant22="printf 'This alias is obsolete. Use dryi (dry init) instead.\n'"
alias dryi="sudo echo 'dry init with dma_test:' && cd ~/dna2_self_test_2_2_0/ && ./setup_3pg.sh ; echo ; printf '\e[1;35m   Ensure that compute blocks 01 and 02 are enabled (verify power or use alias enpg) then ./run_3pg.sh or ./run_3pg.sh 999\e[0m\n\n' ; enpg"
alias d00="~/dna2_self_test_2_2_0/dma_test 0 ddr0 1048576"
alias d01="~/dna2_self_test_2_2_0/dma_test 0 ddr1 1048576"
alias d10="~/dna2_self_test_2_2_0/dma_test 1 ddr0 1048576"
alias d11="~/dna2_self_test_2_2_0/dma_test 1 ddr1 1048576"
alias dma="source ~/HJS/u22/dma22.sh"
alias dma1k="source ~/HJS/u22/dma1k.sh"
alias dmadual="source ~/HJS/u22/dma00d.sh"
alias dmasingle="source ~/HJS/u22/dma00s.sh"
alias dry="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh"
alias dry1="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 9"
alias dry2="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 99"
alias dry3="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 999"
alias dry4="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 9999"
alias dry5="cd ~/dna2_self_test_2_2_0/ && ./run_3pg.sh 99999"
alias trump="source ~/HJS/mfg/trump.sh"
# Version
alias ver="printf '\n\e[1;35m   HJS aliases v3.78\e[0m\n\n'"
# EOF
