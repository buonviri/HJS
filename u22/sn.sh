#!/bin/bash

if [ $# == 2 ]; then
  foo=$(printf "$HOME/S2xx/prodtest/%s/" "$1" )
  bar=$(printf "%s%s" "$1" "$2")
  star=-*
  # echo "DEBUG: $foo $bar"
  valid=$(find "$foo" -name "$bar$star")
  if [ -z "$valid" ]; then
    printf "\n   \e[1;31mSerial number not found: %s%s\e[0m\n" "$1" "$2"
  else
    printf "\nSummary for serial number %s%s" "$1" "$2" # start of summary line
    foobar=$(printf "%s%s" "$foo" "$bar")
    printf " in \e[1;35m$foobar%s\e[0m\n" "$star" # finish the previous line
    printf "Log count: "
    cat $foobar$star | grep -o -i 'board.*edgecortix' | wc -l
    printf "BIST pass: "
    cat $foobar$star | grep -o -i 'bist.*pass' | wc -l
    printf "BIST fail: "
    cat $foobar$star | grep -o -i 'bist.*fail' | wc -l
    printf "DMA pass: "
    cat $foobar$star | grep -o -i 'trial.*pass' | wc -l
    printf "DMA fail: "
    cat $foobar$star | grep -o -i 'trial.*fail' | wc -l
  fi
else
  printf "Usage:\n   Enter the lot code and serial number as parameters.\nExample:\n   sn 12345 001\n"
fi

echo
# EOF

# cat ~/S2xx/prodtest/52979/52979001*
# ls ~/S2xx/prodtest/52979/
# cd ~/S2xx/prodtest/52979/

# "%s%s-0x6797e0df.txt"
# 52979018-0x6797e0df.txt
