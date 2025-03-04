#!/bin/bash

if [ $# == 1 ]; then 
  count=$1
  for (( i=0; i<$count; i++ )); do
    source ~/HJS/mfg/bist.sh 4000  # hopefully this is a good delay
  done
else
  printf "Usage:\n   Enter the number of loops.\nExample:\n   bistn 10\n"
fi

# EOF
