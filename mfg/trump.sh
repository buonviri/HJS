#!/bin/bash

s2i
cd ~/m.2_power_test
printf "\e[1;35minit complete\e[0m -HJS\n"

if [ $# == 1 ]; then 
  count=$1  # set count to arg
else
  count=1  # default to 1
fi

for (( i=0; i<$count; i++ )); do
  echo
  printf "\e[1;32mLoop = $i\e[0m\n"
  echo
  python3 demo_model.py
done

de
cd
echo
s2

# EOF
