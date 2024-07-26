
# ubuntu aliases by HJS v2.22

alias uu="sudo apt update && sudo apt upgrade"
alias bios="systemctl reboot --firmware-setup"
alias snap="killall snap-store && snap refresh"

alias mera="cd ~/S1LP/install_mera/ && source start.sh && mera --version && mera --sakura1_start"
alias camera="cd ~/S1LP/camera && ./RUN_DEMO2_FUSED.sh"

alias sjlog="cd ~/S1LP/inference/ && python3 sjlog.py"
alias ips="source ~/S1LP/inference/ips.sh"

alias fym="cd ~/S1LP/demos/fused_yolov5m_monodepth/ && python deploy.py && python demo_model.py && eog *.png"
alias mde="cd ~/S1LP/demos/monodepth_depth_estimation_demo/ && python deploy.py && python demo_model.py && eog *.png"
alias yod="cd ~/S1LP/demos/yolov5_object_detection_demo/ && python deploy.py && python demo_model.py && eog *.png"

# EOF
