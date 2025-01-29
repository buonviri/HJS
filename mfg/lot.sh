#!/bin/bash
echo

declare -a foo=()  # empty array
if [ $# == 2 ]; then  # expects two args

  lotcode=$1
  count=$2

  if [ $count -lt 1 ]; then
    foo+=("001")  # always do 001
  else
    for (( i=0; i<$count; i++ )); do
      bar=$((i+1))
      formatted=$(printf "%03d\n" $bar)
      foo+=($formatted)
    done
  fi

  for i in "${foo[@]}"; do
    touch "$HOME/S2xx/prodtest/$lotcode/$lotcode$i-xxx.tmp"  # these could be deleted at the end
    zeroruns=$(sn "$lotcode" "$i" | grep "Log count: 0")
    echo Z="$zeroruns"
    sn "$lotcode" "$i" | awk NF  # run the serial number script then format+print
    echo
  done

else  # wrong number of args
  printf "Usage:\n   Enter the lot code and max serial number as parameters.\nExample:\n   lot 12345 5\n"
  echo
fi

# EOF
