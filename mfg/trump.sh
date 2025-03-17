#!/bin/bash

s2i  # initialize MERA
cd ~/mera_package/examples/chatbot/
printf "\e[1;35minit complete\e[0m -HJS\n"

if [ $# -gt 0 ]; then  # one or more args passed
  count=$1  # set count equal to first arg
else
  count=1  # default to 1
fi

if [ $# == 2 ]; then 
  query="--input_txt \"$2\""  # set query to second arg
else
  query="--input_txt \"Tell me about Trump.\""  # default
fi

# get start time
start=$(date +%s%3N)

# iterate
for (( i=0; i<$count; i++ )); do
  now=$(date +%s%3N)
  elapsedms=$((now-start))  # calc elapsed
  elapsed=$(echo "$elapsedms/1000" | bc -l)
  printf "\n\e[1;32mi = $i\nt = $elapsed s\e[0m\n\n"
  echo "$query" | xargs python3 demo_model.py
done

de
cd
echo
s2
now=$(date +%s%3N)
elapsedms=$((now-start))  # calc elapsed
elapsed=$(echo "$elapsedms/1000" | bc -l)
if [ $count == 1 ]; then
  printf "\n\e[1;32mCompleted 1 query.\nt = $elapsed s\e[0m\n\n"
else
  printf "\n\e[1;32mCompleted $i queries.\nt = $elapsed s\e[0m\n\n"
fi

# EOF
