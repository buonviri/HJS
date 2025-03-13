#!/bin/bash
sudo echo  # force root login, not needed for this script but imrpoves the 'ten' alias

# determine folder
if [ -d ~/mera_package/ ]; then
  mera="/home/ec/mera_package"  # use $HOME instead?
else
  mera="/home/ec/S2xx"  # this is only here to support legacy installations
fi

# show timestamp
printf "host time: "  # no newline
date '+%H:%M:%S'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename suffix: $hexstamp
echo  # blank line

printf "01) "
mv -v $mera/examples/detr/result.png $mera/examples/detr/result-$hexstamp.png 2>/dev/null || echo OK
printf "02) "
mv -v $mera/examples/efficient_net_demo/result.png $mera/examples/efficient_net_demo/result-$hexstamp.png 2>/dev/null || echo OK
printf "03) "
mv -v $mera/examples/resnet50/result.png $mera/examples/resnet50/result-$hexstamp.png 2>/dev/null || echo OK

printf "04) "
mv -v $mera/examples/huggingface_image_classification/result.png $mera/examples/huggingface_image_classification/result-$hexstamp.png 2>/dev/null || echo OK
printf "05) "
mv -v $mera/examples/huggingface_image_segmentation/result.png $mera/examples/huggingface_image_segmentation/result-$hexstamp.png 2>/dev/null || echo OK
printf "06) "
mv -v $mera/examples/huggingface_text_classification/result.png $mera/examples/huggingface_text_classification/result-$hexstamp.png 2>/dev/null || echo OK
printf "07) "
mv -v $mera/examples/huggingface_text_gen/result.png $mera/examples/huggingface_text_gen/result-$hexstamp.png 2>/dev/null || echo OK

printf "08) "
mv -v $mera/examples/yolov5/result.png $mera/examples/yolov5/result-$hexstamp.png 2>/dev/null || echo OK
printf "09) "
mv -v $mera/examples/yolov7/result.png $mera/examples/yolov7/result-$hexstamp.png 2>/dev/null || echo OK

printf "10a) "
mv -v $mera/examples/yolov8/result_1.png $mera/examples/yolov8/result_1-$hexstamp.png 2>/dev/null || echo OK  # filename contains underscore one!
printf "10b) "
mv -v $mera/examples/yolov8/result.png $mera/examples/yolov8/result-$hexstamp.png 2>/dev/null || echo OK  # filename DOES NOT contain underscore one!

echo
# EOF
