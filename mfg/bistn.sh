#!/bin/bash

if [ $# == 1 ]; then 
  count=$1
  for (( i=0; i<$count; i++ )); do
    source ~/HJS/mfg/bist.sh
  done
else
  printf "Usage:\n   Enter the number of loops.\nExample:\n   bistn 10\n"
fi

# EOF
