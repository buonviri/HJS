#!/bin/bash

function green () {
  printf "\e[1;32m%b\e[0m" "$1"
}

# start with newline
echo

if [ $# == 1 ]; then 
  count=$1
  for (( i=0; i<$count; i++ )); do
    green "[i=$i]\n"
    source ~/HJS/mfg/bist.sh 4000  # hopefully this is a good delay
  done
else
  printf "Usage:\n   Enter the number of loops.\nExample:\n   bistn 10\n"
fi

# EOF
