#!/bin/bash

cd ~/S1LP/demos/yolov5_object_detection_demo/
python deploy.py
python demo_model.py
cd "$OLDPWD"

# EOF
