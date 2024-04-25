#!/bin/bash

cd ~/S1LP/install_mera/ && source start.sh && mera --sakura1_start

# make sure this was done once:
# cd ~/S1LP/inference/test/run_resnet50 && python3 deploy.py

cd ~/S1LP/inference/test/run_resnet50 && python run_resnet50.py --target ip --forever --log --inference_freq 3

# EOF
