#!/bin/bash

s2i
cd ~/m.2_power_test
printf "\e[1;35minit complete\e[0m -HJS\n"

if [ $# -gt 0 ]; then  # one or more args passed
  count=$1  # set count to arg
else
  count=1  # default to 1
fi

if [ $# == 2 ]; then 
  query=" --input_txt '$2' "  # set query to arg
else
  query=" --input_txt 'Tell me about Trump.' "  # default LOL
fi

for (( i=0; i<$count; i++ )); do
  echo
  printf "\e[1;32mi = $i\e[0m\n"
  echo
  python3 demo_model.py "$query"
done

de
cd
echo
s2

# EOF
