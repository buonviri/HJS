#!/bin/bash

cd ~/S1LP/demos/monodepth_depth_estimation_demo/
python deploy.py
python demo_model.py
cd "$OLDPWD"

# EOF
