#!/bin/bash

echo

echo Testing for four pages...
expected="4"
n=$(\grep -o -P "HugePages_Total.*\K[0-9]+$" /proc/meminfo)
if [ "$n" == "$expected" ]; then
  printf "Total HugePages = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m Total HugePages = %s\n" "$n"
fi
n=$(\grep -o -P "HugePages_Free.*\K[0-9]+$" /proc/meminfo)
if [ "$n" == "$expected" ]; then
  printf "Free HugePages = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m Free HugePages = %s\n" "$n"
fi

echo

echo Testing for one page...
expected="1"
n=$(\grep -o -P "HugePages_Total.*\K[0-9]+$" /proc/meminfo)
if [ "$n" == "$expected" ]; then
  printf "Total HugePages = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m Total HugePages = %s\n" "$n"
fi
n=$(\grep -o -P "HugePages_Free.*\K[0-9]+$" /proc/meminfo)
if [ "$n" == "$expected" ]; then
  printf "Free HugePages = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m Free HugePages = %s\n" "$n"
fi

echo

sudo dmesg | grep -i -E "pcie_aspm=|kernel command line:|command line:|default_hugepagesz=|hugepagesz=|hugepages=|iommu="

echo

# EOF
