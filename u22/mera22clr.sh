#!/bin/bash

# show timestamp
echo host time:
date '+%H:%M:%S'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename suffix : $hexstamp

mv ~/S2xx/examples/detr/result.png ~/S2xx/examples/detr/result-$hexstamp.png
mv ~/S2xx/examples/efficient_net_demo/result.png ~/S2xx/examples/efficient_net_demo/result-$hexstamp.png
mv ~/S2xx/examples/resnet50/result.png ~/S2xx/examples/resnet50/result-$hexstamp.png

mv ~/S2xx/examples/huggingface_image_classification/result.png ~/S2xx/examples/huggingface_image_classification/result-$hexstamp.png
mv ~/S2xx/examples/huggingface_image_segmentation/result.png ~/S2xx/examples/huggingface_image_segmentation/result-$hexstamp.png
mv ~/S2xx/examples/huggingface_text_classification/result.png ~/S2xx/examples/huggingface_text_classification/result-$hexstamp.png
mv ~/S2xx/examples/huggingface_text_gen/result.png ~/S2xx/examples/huggingface_text_gen/result-$hexstamp.png

mv ~/S2xx/examples/yolov5/result.png ~/S2xx/examples/yolov5/result-$hexstamp.png
mv ~/S2xx/examples/yolov7/result.png ~/S2xx/examples/yolov7/result-$hexstamp.png
mv ~/S2xx/examples/yolov8/result_1.png ~/S2xx/examples/yolov8/result_1-$hexstamp.png  # underscore one!

# EOF
