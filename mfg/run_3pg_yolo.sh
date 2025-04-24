#!/bin/bash

# removed everything but yolo
# setup:
# cd ~/dna2_self_test_2_2_0/ && chmod +x ./run_3pg_yolo.sh
# run using:
# dryi && cd ~/dna2_self_test_2_2_0/ && ./run_3pg_yolo.sh 99999

NTIMES="${1:-2}"
DEVICE_ID="${2:-0}"
# printf "\n   \e[1;32m[DETR]\e[0m\n\n"
# LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/detr_3pg/ ${NTIMES}
# printf "\n   \e[1;32m[ResNet50]\e[0m\n\n"
# LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/resnet50_3pg/ ${NTIMES}
printf "\n   \e[1;32m[YoloV8]\e[0m\n\n"
LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/yolov8m_3pg/ ${NTIMES}
echo

# EOF
