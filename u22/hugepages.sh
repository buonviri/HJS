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
sudo dmesg | GREP_COLORS='ms=01;32' grep --color=auto -i -E "pcie_aspm=|kernel command line:|command line:|default_hugepagesz=|hugepagesz=|hugepages=|iommu="
echo

echo Testing for pt (should pass)...
expected="pt"
n=$(sudo dmesg | \grep -i -o -P "kernel command line.*iommu=\K[a-z][a-z]")
if [ "$n" == "$expected" ]; then
  printf "iommu = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m iommu = %s\n" "$n"
fi
echo
echo Testing for xx (should fail)...
expected="xx"
n=$(sudo dmesg | \grep -i -o -P "kernel command line.*iommu=\K[a-z][a-z]")
if [ "$n" == "$expected" ]; then
  printf "iommu = %s \e[1;32m(OK)\e[0m\n" "$n"
else
  printf "\e[1;31mWARNING!\e[0m iommu = %s\n" "$n"
fi

echo

# EOF
