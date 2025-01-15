#!/bin/bash

# show timestamp
echo host time:
date '+%H:%M:%S'

# timestamp
time_t=$(date +%s)
hexstamp=$(printf "%x" $time_t)
echo Filename suffix : $hexstamp

mv ~/S2xx/examples/detr/result.png ~/S2xx/examples/detr/result-$hexstamp.png 

# EOF
