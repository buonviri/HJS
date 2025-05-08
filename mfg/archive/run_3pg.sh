#!/bin/bash

# edited by HJS to separate sections more clearly

NTIMES="${1:-2}"
DEVICE_ID="${2:-0}"
printf "\n   \e[1;32m[DETR]\e[0m\n\n"
LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/detr_3pg/ ${NTIMES}
printf "\n   \e[1;32m[ResNet50]\e[0m\n\n"
LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/resnet50_3pg/ ${NTIMES}
printf "\n   \e[1;32m[YoloV8]\e[0m\n\n"
LD_LIBRARY_PATH=./ OMP_NUM_THREADS=1  ./executor ${DEVICE_ID} ./deployments_3pg/yolov8m_3pg/ ${NTIMES}
echo

# EOF
