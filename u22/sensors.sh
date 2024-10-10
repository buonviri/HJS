#!/bin/bash

function add_module () {
  caret=$(printf "^%s" "$1")  # insert caret before string, for grep
  match=$(grep "$caret" /etc/modules)  # check for match (should be blank or exact string)
  printf "\nsensor: %s\n" "$1"
  printf "regex: %s\n" "$caret"
  printf "grep:   %s\n" "$match"
  if [[ "$match" == "$1" ]]; then  # exit 0 means match was found
    printf "/etc/modules already contains %s\n" "$1"
  else
    printf "/etc/modules: adding %s\n" "$1"
    printf "\n# EdgeCortix - %s\n%s\n" "$(date)" "$1" | sudo tee -a /etc/modules
  fi
}

mobo=$(cat /sys/devices/virtual/dmi/id/board_name)
# echo "$mobo"

if [[ "$mobo" == "X600-ITX" ]]; then  # ASRock X600 (AMD)
  echo X600 sensor configuration:
  for sensor in lm92 nct6775  # note that this is NOT the list found by sensors-detect, but is required for fan info
  do 
    add_module "$sensor"
  done
elif [[ "$mobo" == "X300-ITX" ]]; then  # ASRock X300 (AMD)
  echo X300 sensor configuration:
  for sensor in nct6775
  do 
    add_module "$sensor"
  done
elif [[ "$mobo" == "sbc-flt3" ]]; then  # fitlet3 (Atom)
  echo fitlet3 sensor configuration:
  for sensor in coretemp
  do 
    add_module "$sensor"
  done
elif [[ "$mobo" == "0VXN07" ]]; then  # Dell Optiplex (Intel)
  echo Dell Optiplex sensor configuration:
  for sensor in coretemp
  do 
    add_module "$sensor"
  done
else
  printf "Unknown system (%s)... skipping sensor configuration.\n" "$mobo"
fi

# the end
