#!/bin/bash

s2i  # initialize MERA
cd ~/m.2_power_test
printf "\e[1;35minit complete\e[0m -HJS\n"

if [ $# -gt 0 ]; then  # one or more args passed
  count=$1  # set count to first arg
else
  count=1  # default to 1
fi

if [ $# == 2 ]; then 
  query="--input_txt \"$2\""  # set query to second arg
else
  query="--input_txt \"Tell me about Trump.\""  # default
fi

for (( i=0; i<$count; i++ )); do
  printf "\n\e[1;32mi = $i\e[0m\n\n"
  echo "$query" | xargs python3 demo_model.py
done

de
cd
echo
s2
if [ $count == 1 ]; then
  printf "\n\e[1;32mCompleted 1 query.\e[0m\n\n"
else
  printf "\n\e[1;32mCompleted $i queries.\e[0m\n\n"
fi

# EOF
